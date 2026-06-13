# filepath: src/services/tasks.py

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from config import settings
from db.base import utcnow
from db.models import Jump, JumpStatus, Task, TaskStatus, User
from schemas.task import TaskCreate
from services import matching
from services.attributes import load_snapshot

# Jump states that consume a Jumper slot.
_SLOT_STATES = (JumpStatus.ACTIVE.value, JumpStatus.SUBMITTED.value, JumpStatus.VERIFIED.value)


def launch_task(db: Session, owner: User, data: TaskCreate) -> Task:
    task = Task(
        owner_id=owner.id,
        desc=data.desc,
        total_budget=data.total_budget,
        you_earn=data.you_earn,
        num_jumpers=data.num_jumpers,
        category=data.category,
        accept_jumpers_manually=data.accept_jumpers_manually,
        launcher_review=data.launcher_review,
        # exclude_unset: persist exactly what the Launcher sent, nothing synthesized
        filters=data.filters.model_dump(exclude_unset=True) if data.filters else None,
        operation_requirements=data.operation_requirements,
        other_requirements=data.other_requirements,
        partition_deadline=data.partition_deadline,
        submission_deadline=data.submission_deadline,
        status=TaskStatus.OPEN.value,
    )
    db.add(task)
    db.flush()
    return task


def get_task(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    return task


def browse_tasks(
    db: Session,
    *,
    viewer_id: int | None = None,
    status_filter: str | None = None,
    category: str | None = None,
    min_you_earn: float | None = None,
    page: int = 1,
    size: int = 20,
) -> tuple[list[Task], int]:
    q = db.query(Task)
    if status_filter is not None:
        q = q.filter(Task.status == status_filter)
    if category is not None:
        q = q.filter(Task.category == category)
    if min_you_earn is not None:
        q = q.filter(Task.you_earn >= min_you_earn)
    q = q.order_by(Task.creation_date.desc(), Task.id.desc())

    if viewer_id is None:
        # unfiltered path (internal callers)
        return q.offset((page - 1) * size).limit(size).all(), q.count()

    # Eligible feed (matching C3): per-task filters mean eligibility can't be
    # one WHERE clause — load the viewer's snapshot once, evaluate in Python
    # over a bounded scan, then paginate the eligible list.
    candidates = q.limit(settings.BROWSE_SCAN_LIMIT).all()
    snapshot = load_snapshot(db, viewer_id)
    eligible = [
        t
        for t in candidates
        if not matching.unmet_requirements(matching.parse_filters(t.filters), snapshot)
    ]
    return eligible[(page - 1) * size : page * size], len(eligible)


def my_tasks(db: Session, owner_id: int) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.owner_id == owner_id)
        .order_by(Task.creation_date.desc(), Task.id.desc())
        .all()
    )


def participated(db: Session, jumper_id: int) -> list[Jump]:
    return (
        db.query(Jump)
        .options(joinedload(Jump.task))
        .filter(Jump.jumper_id == jumper_id)
        .order_by(Jump.created_at.desc(), Jump.id.desc())
        .all()
    )


def _occupied_slots(db: Session, task_id: int) -> int:
    return (
        db.query(func.count(Jump.id))
        .filter(Jump.task_id == task_id, Jump.status.in_(_SLOT_STATES))
        .scalar()
    )


def jump_on_task(db: Session, task: Task, jumper: User) -> Jump:
    if task.status != TaskStatus.OPEN.value:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Task is {task.status}, not open")
    if task.owner_id == jumper.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot jump on your own task")
    existing = db.query(Jump).filter(Jump.task_id == task.id, Jump.jumper_id == jumper.id).first()
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Already jumped on this task")

    # Eligibility gate (matching C2): verified attributes must pass the
    # task's filters. Unfiltered tasks match everyone.
    ok, unmet = matching.user_matches(db, task.filters, jumper.id)
    if not ok:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"You don't match this task's requirements: {', '.join(unmet)}",
        )

    if task.accept_jumpers_manually:
        jump = Jump(task_id=task.id, jumper_id=jumper.id, status=JumpStatus.PENDING.value)
    else:
        if _occupied_slots(db, task.id) >= task.num_jumpers:
            raise HTTPException(status.HTTP_409_CONFLICT, "Task is full")
        jump = Jump(
            task_id=task.id,
            jumper_id=jumper.id,
            status=JumpStatus.ACTIVE.value,
            approved_at=utcnow(),
        )
    db.add(jump)
    db.flush()

    if _occupied_slots(db, task.id) >= task.num_jumpers:
        task.status = TaskStatus.FULL.value
    return jump


def list_jumps(
    db: Session, task: Task, owner: User, status_filter: str | None = None
) -> list[Jump]:
    if task.owner_id != owner.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the Launcher can list a task's jumps")
    q = db.query(Jump).filter(Jump.task_id == task.id)
    if status_filter is not None:
        q = q.filter(Jump.status == status_filter)
    return q.order_by(Jump.created_at.asc(), Jump.id.asc()).all()


def reject_jump(db: Session, task: Task, owner: User, jump_id: int) -> Jump:
    """Launcher declines a pending Jumper — symmetric to approve_jump."""
    if task.owner_id != owner.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the Launcher can reject Jumpers")
    jump = db.get(Jump, jump_id)
    if jump is None or jump.task_id != task.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Jump not found")
    if jump.status != JumpStatus.PENDING.value:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Jump is {jump.status}, not pending")

    jump.status = JumpStatus.REJECTED.value
    jump.resolved_at = utcnow()
    return jump


def approve_jump(db: Session, task: Task, owner: User, jump_id: int) -> Jump:
    if task.owner_id != owner.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the Launcher can approve Jumpers")
    jump = db.get(Jump, jump_id)
    if jump is None or jump.task_id != task.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Jump not found")
    if jump.status != JumpStatus.PENDING.value:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Jump is {jump.status}, not pending")
    if _occupied_slots(db, task.id) >= task.num_jumpers:
        raise HTTPException(status.HTTP_409_CONFLICT, "Task is full")

    jump.status = JumpStatus.ACTIVE.value
    jump.approved_at = utcnow()
    db.flush()

    if _occupied_slots(db, task.id) >= task.num_jumpers:
        task.status = TaskStatus.FULL.value
    return jump


def forfeit_jump(db: Session, task: Task, jumper: User) -> Jump:
    jump = db.query(Jump).filter(Jump.task_id == task.id, Jump.jumper_id == jumper.id).first()
    if jump is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "You have not jumped on this task")
    if jump.status not in (JumpStatus.PENDING.value, JumpStatus.ACTIVE.value):
        raise HTTPException(status.HTTP_409_CONFLICT, f"Cannot forfeit a {jump.status} jump")

    jump.status = JumpStatus.FORFEITED.value
    jump.resolved_at = utcnow()
    db.flush()

    # A freed slot reopens a full task.
    if task.status == TaskStatus.FULL.value and _occupied_slots(db, task.id) < task.num_jumpers:
        task.status = TaskStatus.OPEN.value
    return jump
