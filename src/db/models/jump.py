# filepath: src/db/models/jump.py

import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.base import Base, utcnow


class JumpStatus(str, enum.Enum):
    PENDING = "pending"  # waiting for Launcher approval (accept_jumpers_manually)
    ACTIVE = "active"  # approved / auto-approved; Jumper is performing
    SUBMITTED = "submitted"  # proof uploaded, awaiting verification
    VERIFIED = "verified"  # completion verified
    REJECTED = "rejected"  # proof rejected, or Jumper not approved
    FORFEITED = "forfeited"  # Jumper backed out


class Jump(Base):
    """A Jumper's participation in a Task — the table the old schema never had."""

    __tablename__ = "jumps"
    __table_args__ = (UniqueConstraint("task_id", "jumper_id"),)

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False, index=True)
    jumper_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    status = Column(String(20), nullable=False, default=JumpStatus.ACTIVE.value, index=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)  # verified/rejected/forfeited

    task = relationship("Task", back_populates="jumps")
    jumper = relationship("User", back_populates="jumps")

    def __repr__(self) -> str:
        return f"<Jump id={self.id} task={self.task_id} jumper={self.jumper_id} {self.status}>"
