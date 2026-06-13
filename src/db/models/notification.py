# filepath: src/db/models/notification.py

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Index, Integer, String

from db.base import Base, utcnow


class Notification(Base):
    """Ledger of every outbound notification (matching C9).

    dedupe_key (unique) is the idempotency guarantee: the same event for the
    same user can never notify twice, even across retries or relaunches.
    """

    __tablename__ = "notifications"
    __table_args__ = (Index("ix_notifications_user_created", "user_id", "created_at"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    text = Column(String(500), nullable=True)  # the rendered message, for audit + web polling
    payload = Column(JSON, nullable=True)
    status = Column(String(16), nullable=False, default="pending")
    # pending | sent | failed | skipped
    skip_reason = Column(String(30), nullable=True)  # "muted" | "no_channel"
    dedupe_key = Column(String(120), nullable=True, unique=True)
    provider_ref = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    sent_at = Column(DateTime(timezone=True), nullable=True)
