# filepath: src/routers/users.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from db.deps import get_db
from db.models import Notification, User, UserVerification
from routers.deps import get_current_user
from schemas.user import NotificationPrefs, NotificationRead, UserMe, VerificationSummary

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/notifications", response_model=list[NotificationRead])
def my_notifications(
    since_id: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Notification]:
    """The caller's notification ledger, newest first. Poll with since_id =
    highest id you've seen to fetch only what's new."""
    q = db.query(Notification).filter(Notification.user_id == user.id)
    if since_id:
        q = q.filter(Notification.id > since_id)
    return q.order_by(Notification.id.desc()).limit(limit).all()


@router.post("/me/notifications", response_model=NotificationPrefs)
def set_notification_prefs(
    body: NotificationPrefs,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NotificationPrefs:
    user.notifications_muted = body.muted
    return NotificationPrefs(muted=body.muted)


@router.get("/me", response_model=UserMe)
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> UserMe:
    verifications = (
        db.query(UserVerification)
        .options(joinedload(UserVerification.verification_type))
        .filter(UserVerification.user_id == user.id)
        .all()
    )
    return UserMe(
        id=user.id,
        email=user.email,
        name=user.name,
        telegram_handle=user.telegram_handle,
        is_email_verified=user.is_email_verified,
        phone_number=user.phone_number,
        is_phone_verified=user.phone_verified_at is not None,
        notifications_muted=user.notifications_muted,
        created_at=user.created_at,
        verifications=[
            VerificationSummary(
                verification_name=v.verification_type.verification_name,
                status=v.status,
                expires_at=v.expires_at,
            )
            for v in verifications
        ],
        trust_score=None,
    )
