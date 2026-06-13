# filepath: src/db/models/task.py

import enum

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from db.base import Base, utcnow


class TaskStatus(str, enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    FULL = "full"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    desc = Column(Text, nullable=False)
    total_budget = Column(Float, nullable=False, default=0.0)
    you_earn = Column(Float, nullable=False, default=0.0)  # per-Jumper pay
    num_jumpers = Column(Integer, nullable=False, default=1)
    status = Column(String(20), nullable=False, default=TaskStatus.OPEN.value, index=True)
    category = Column(String(50), nullable=True, index=True)

    accept_jumpers_manually = Column(Boolean, nullable=False, default=False)
    launcher_review = Column(Boolean, nullable=False, default=False)

    # Clarifier output contract (catalog §6): the consensus snapshot's
    # normalized slots (actions, end_state, bound, target) copied from the
    # approved run at launch; null for tasks launched via direct POST /tasks.
    normalized_slots = Column(JSON, nullable=True)
    # use_alter breaks the FK cycle tasks -> clarifier_runs -> task_drafts -> tasks
    clarifier_run_id = Column(
        Integer, ForeignKey("clarifier_runs.id", use_alter=True), nullable=True
    )

    # Persisted verbatim as submitted; structure per devdocs/filter_design.md.
    filters = Column(JSON, nullable=True)
    operation_requirements = Column(JSON, nullable=True)
    other_requirements = Column(JSON, nullable=True)

    creation_date = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    partition_deadline = Column(DateTime(timezone=True), nullable=True)
    submission_deadline = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="tasks")
    jumps = relationship("Jump", back_populates="task")

    def __repr__(self) -> str:
        return f"<Task id={self.id} status={self.status}>"
