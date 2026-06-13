# filepath: src/services/audit.py

from sqlalchemy.orm import Session

from db.models import AuditEvent


def record(
    db: Session,
    event_type: str,
    actor_id: int | None = None,
    target_type: str | None = None,
    target_id: int | None = None,
    payload: dict | None = None,
    request_id: str | None = None,
) -> None:
    """Append one audit event. Committed with the surrounding request transaction."""
    db.add(
        AuditEvent(
            event_type=event_type,
            actor_id=actor_id,
            target_type=target_type,
            target_id=target_id,
            payload=payload,
            request_id=request_id,
        )
    )
