# filepath: src/routers/tasks.py

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import User
from routers.deps import get_current_user
from schemas.common import Page
from schemas.task import (
    AudiencePreviewRequest,
    AudiencePreviewResponse,
    JumpRead,
    ParticipationRead,
    TaskCreate,
    TaskRead,
)
from services import audit, notifications
from services import tasks as task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


@router.post("", response_model=TaskRead, status_code=201)
def launch_task(
    body: TaskCreate,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskRead:
    task = task_service.launch_task(db, user, body)
    audit.record(
        db,
        "task.launched",
        actor_id=user.id,
        target_type="task",
        target_id=task.id,
        payload={"total_budget": task.total_budget, "num_jumpers": task.num_jumpers},
        request_id=_request_id(request),
    )
    notifications.fan_out_task_matched(db, task)  # matching C7
    return task


@router.get("", response_model=Page[TaskRead])
def browse_tasks(
    status: str | None = Query(default=None),
    category: str | None = Query(default=None),
    min_you_earn: float | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Page[TaskRead]:
    items, total = task_service.browse_tasks(
        db,
        viewer_id=user.id,
        status_filter=status,
        category=category,
        min_you_earn=min_you_earn,
        page=page,
        size=size,
    )
    return Page(
        items=[TaskRead.model_validate(t) for t in items],
        total=total,
        page=page,
        size=size,
    )


@router.post("/audience-preview", response_model=AudiencePreviewResponse)
def audience_preview(
    body: AudiencePreviewRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AudiencePreviewResponse:
    """How many verified Jumpers match these filters — shown to the Launcher
    before funding. Exact counts only above the privacy floor."""
    from config import settings
    from services import matching

    filters = body.filters.model_dump(exclude_unset=True) if body.filters else None
    count, warnings = matching.audience_count(db, filters, exclude_user_id=user.id)
    if count < settings.AUDIENCE_PRIVACY_FLOOR:
        return AudiencePreviewResponse(
            eligible_count=None,
            display=f"fewer than {settings.AUDIENCE_PRIVACY_FLOOR}",
            warnings=warnings,
        )
    return AudiencePreviewResponse(eligible_count=count, display=str(count), warnings=warnings)


@router.get("/my", response_model=list[TaskRead])
def my_tasks(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[TaskRead]:
    return task_service.my_tasks(db, user.id)


@router.get("/participated", response_model=list[ParticipationRead])
def participated_tasks(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[ParticipationRead]:
    jumps = task_service.participated(db, user.id)
    return [
        ParticipationRead(jump=JumpRead.model_validate(j), task=TaskRead.model_validate(j.task))
        for j in jumps
    ]


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskRead:
    return task_service.get_task(db, task_id)


@router.post("/{task_id}/jump", response_model=JumpRead, status_code=201)
def jump_on_task(
    task_id: int,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JumpRead:
    task = task_service.get_task(db, task_id)
    jump = task_service.jump_on_task(db, task, user)
    audit.record(
        db,
        "task.jumped",
        actor_id=user.id,
        target_type="jump",
        target_id=jump.id,
        payload={"task_id": task.id, "status": jump.status},
        request_id=_request_id(request),
    )
    if jump.status == "pending":
        notifications.notify_jump_pending(db, task, jump)
    if task.status == "full":
        notifications.notify_task_full(db, task)
    return jump


@router.get("/{task_id}/jumps", response_model=list[JumpRead])
def list_task_jumps(
    task_id: int,
    status: str | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[JumpRead]:
    task = task_service.get_task(db, task_id)
    return task_service.list_jumps(db, task, user, status_filter=status)


@router.post("/{task_id}/jumps/{jump_id}/reject", response_model=JumpRead)
def reject_jump(
    task_id: int,
    jump_id: int,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JumpRead:
    task = task_service.get_task(db, task_id)
    jump = task_service.reject_jump(db, task, user, jump_id)
    audit.record(
        db,
        "task.jump_rejected",
        actor_id=user.id,
        target_type="jump",
        target_id=jump.id,
        payload={"task_id": task.id},
        request_id=_request_id(request),
    )
    notifications.notify_jump_decision(db, task, jump, approved=False)
    return jump


@router.post("/{task_id}/jumps/{jump_id}/approve", response_model=JumpRead)
def approve_jump(
    task_id: int,
    jump_id: int,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JumpRead:
    task = task_service.get_task(db, task_id)
    jump = task_service.approve_jump(db, task, user, jump_id)
    audit.record(
        db,
        "task.jump_approved",
        actor_id=user.id,
        target_type="jump",
        target_id=jump.id,
        payload={"task_id": task.id},
        request_id=_request_id(request),
    )
    notifications.notify_jump_decision(db, task, jump, approved=True)
    if task.status == "full":
        notifications.notify_task_full(db, task)
    return jump


@router.post("/{task_id}/forfeit", response_model=JumpRead)
def forfeit(
    task_id: int,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JumpRead:
    task = task_service.get_task(db, task_id)
    jump = task_service.forfeit_jump(db, task, user)
    audit.record(
        db,
        "task.forfeited",
        actor_id=user.id,
        target_type="jump",
        target_id=jump.id,
        payload={"task_id": task.id},
        request_id=_request_id(request),
    )
    return jump
