# filepath: src/db/models/audit.py

from sqlalchemy import JSON, Column, DateTime, Index, Integer, String

from db.base import Base, utcnow


class AuditEvent(Base):
    """Event-based audit log: one row per significant platform action.

    Lives on the same Base/metadata as everything else — the old project's
    log model had its own orphaned declarative Base and never made it into
    the schema.
    """

    __tablename__ = "audit_events"
    __table_args__ = (
        Index("ix_audit_type_time", "event_type", "created_at"),
        Index("ix_audit_actor_time", "actor_id", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    event_type = Column(String(50), nullable=False)  # e.g. "auth.register", "task.launched"
    actor_id = Column(Integer, nullable=True)  # user id; NULL for system
    target_type = Column(String(30), nullable=True)  # "task" | "user" | "jump" | "payment"
    target_id = Column(Integer, nullable=True)
    payload = Column(JSON, nullable=True)
    request_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
