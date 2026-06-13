# filepath: src/services/notifications.py

"""Notification ledger + event fan-out (matching C7 + C9).

Every outbound message gets a ledger row first; dedupe_key makes events
idempotent. Delivery failures mark the row failed and never break the
request that triggered them.
"""

import logging

from sqlalchemy.orm import Session

from config import settings
from db.base import utcnow
from db.models import Jump, Notification, Task, User
from services import matching
from services.notifier import get_notifier

logger = logging.getLogger(__name__)

TASK_MATCHED = '🐦 New task for you: "{desc}" — earn {you_earn} USDT each. See /browse'
JUMP_APPROVED = "✅ You were approved for task #{task_id}! Perform it and submit proof via /myjumps"
JUMP_REJECTED = "❌ The Launcher declined your application for task #{task_id}."
JUMP_PENDING = "⏳ A Jumper applied to your task #{task_id} — approve or decline in /mytasks"
TASK_FULL = "🔵 Your task #{task_id} is full — all {num_jumpers} slot(s) taken."


def notify(
    db: Session,
    user: User,
    event_type: str,
    text: str,
    dedupe_key: str | None = None,
    payload: dict | None = None,
) -> Notification | None:
    """Ledger + deliver. Returns None when deduped, the row otherwise."""
    if dedupe_key is not None:
        exists = db.query(Notification).filter(Notification.dedupe_key == dedupe_key).first()
        if exists is not None:
            return None

    row = Notification(
        user_id=user.id, event_type=event_type, text=text, payload=payload, dedupe_key=dedupe_key
    )
    db.add(row)
    db.flush()

    if user.notifications_muted:
        row.status, row.skip_reason = "skipped", "muted"
        return row
    if settings.NOTIFY_BACKEND == "telegram" and not user.telegram_id:
        row.status, row.skip_reason = "skipped", "no_channel"
        return row

    chat_id = user.telegram_id or str(user.id)
    try:
        row.provider_ref = get_notifier().send(chat_id, text)
        row.status = "sent"
        row.sent_at = utcnow()
    except Exception as e:  # delivery must never break the triggering request
        logger.warning("Notification %s to user %s failed: %s", event_type, user.id, e)
        row.status = "failed"
    return row


def fan_out_task_matched(db: Session, task: Task) -> int:
    """Notify matched Jumpers on launch (C7), capped, newest accounts first."""
    q, _warnings = matching.audience_query(db, task.filters)
    recipients = (
        q.filter(User.id != task.owner_id)
        .order_by(User.created_at.desc(), User.id.desc())
        .limit(settings.MATCH_NOTIFY_CAP)
        .all()
    )
    for user in recipients:
        notify(
            db,
            user,
            "task.matched",
            TASK_MATCHED.format(desc=task.desc[:80], you_earn=task.you_earn),
            dedupe_key=f"task.matched:{task.id}:{user.id}",
            payload={"task_id": task.id},
        )
    return len(recipients)


def notify_jump_pending(db: Session, task: Task, jump: Jump) -> None:
    notify(
        db,
        task.owner,
        "jump.pending",
        JUMP_PENDING.format(task_id=task.id),
        dedupe_key=f"jump.pending:{jump.id}",
        payload={"task_id": task.id, "jump_id": jump.id},
    )


def notify_jump_decision(db: Session, task: Task, jump: Jump, approved: bool) -> None:
    jumper = db.get(User, jump.jumper_id)
    if jumper is None:
        return
    event = "jump.approved" if approved else "jump.rejected"
    template = JUMP_APPROVED if approved else JUMP_REJECTED
    notify(
        db,
        jumper,
        event,
        template.format(task_id=task.id),
        dedupe_key=f"{event}:{jump.id}",
        payload={"task_id": task.id, "jump_id": jump.id},
    )


def notify_task_full(db: Session, task: Task) -> None:
    notify(
        db,
        task.owner,
        "task.full",
        TASK_FULL.format(task_id=task.id, num_jumpers=task.num_jumpers),
        dedupe_key=f"task.full:{task.id}",
        payload={"task_id": task.id},
    )
