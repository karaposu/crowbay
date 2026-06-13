# filepath: src/db/models/clarifier.py

import enum

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from db.base import Base, utcnow


class DraftStatus(str, enum.Enum):
    CLARIFYING = "clarifying"
    AWAITING_APPROVAL = "awaiting_approval"
    HELD = "held"
    DECLINED = "declined"
    ABANDONED = "abandoned"
    LAUNCHED = "launched"


class TaskDraft(Base):
    """A task submission inside the clarifier loop (BOM §1).

    Status machine (transitions enforced server-side in the lifecycle
    endpoints, BOM §6):

        clarifying ──run ok, no gate──▶ awaiting_approval ──approve──▶ launched
        clarifying ──CJ-K3 uncertain──▶ held ──operator──▶ awaiting_approval | declined
        clarifying ──unrepairable gate─▶ declined (revise may re-enter clarifying)
        any pre-launch state ──cancel/silence──▶ abandoned

    Drafts are deliberately NOT rows on `tasks` — browse/my_tasks carry no
    status guard, so draft rows would leak into existing surfaces (see the
    BOM's decisions table). `task_id` links the launched task once approved.
    """

    __tablename__ = "task_drafts"
    __table_args__ = (Index("ix_task_drafts_owner_created", "owner_id", "created_at"),)

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    # The submitted TaskCreate-shaped payload, verbatim (desc + fields).
    payload = Column(JSON, nullable=False)
    status = Column(
        String(20), nullable=False, default=DraftStatus.CLARIFYING.value, index=True
    )
    # Client-generated dedupe key (Telegram double-taps); unique when present.
    idempotency_key = Column(String(120), nullable=True, unique=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow
    )

    owner = relationship("User")
    runs = relationship(
        "ClarifierRun", back_populates="draft", order_by="ClarifierRun.id"
    )

    def __repr__(self) -> str:
        return f"<TaskDraft id={self.id} status={self.status}>"


class ClarifierRun(Base):
    """One engine pass over one submission revision (BOM §1).

    (draft_id, submission_hash) is unique — the idempotency guarantee:
    revising with unchanged text returns the cached run instead of a new
    LLM call (catalog §2.5). `card_payload` is persisted as-shown: it IS
    the consent record the approval snapshot references (catalog §5.4).
    """

    __tablename__ = "clarifier_runs"
    __table_args__ = (
        UniqueConstraint("draft_id", "submission_hash", name="uq_clarifier_runs_draft_hash"),
    )

    id = Column(Integer, primary_key=True)
    draft_id = Column(Integer, ForeignKey("task_drafts.id"), nullable=False, index=True)
    submission_hash = Column(String(64), nullable=False)
    catalog_version = Column(String(16), nullable=False)
    backend = Column(String(16), nullable=False)  # off | mock | real
    status = Column(String(16), nullable=False, default="complete")
    # complete | degraded (LLM unavailable -> code-only; audit clarifier.skipped)
    llm_output = Column(JSON, nullable=True)  # null when off/degraded
    card_payload = Column(JSON, nullable=True)  # the card as shown (consent record)
    normalized_slots = Column(JSON, nullable=True)  # copied onto the task at launch
    # ToS matrix v1 row — logged on EVERY run (matrix-v2 calibration data).
    tos_category = Column(String(16), nullable=True, index=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    draft = relationship("TaskDraft", back_populates="runs")
    detections = relationship(
        "DetectionRecord", back_populates="run", order_by="DetectionRecord.id"
    )

    def __repr__(self) -> str:
        return f"<ClarifierRun id={self.id} draft={self.draft_id} status={self.status}>"


class DetectionRecord(Base):
    """Per-entry result row (catalog §2.6) — the calibration dataset.

    References the run; never copies submission text (PII stays on the
    draft, once). `resolution` is updated after the run as the Launcher
    interacts: accepted-chip | typed-answer | stet | override | abandoned | n-a.
    Unknown codes in old rows are tolerated by readers (registry tolerance).
    """

    __tablename__ = "detection_records"
    __table_args__ = (Index("ix_detection_records_code_result", "code", "result"),)

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("clarifier_runs.id"), nullable=False, index=True)
    code = Column(String(12), nullable=False)  # e.g. CJ-I7; registry is the namespace
    entry_version = Column(Integer, nullable=False, default=1)
    result = Column(String(16), nullable=False)
    # clear | fired | uncertain | not-evaluated
    severity_at_fire = Column(String(10), nullable=True)  # gate | clarify | warn
    response_shown = Column(JSON, nullable=True)  # what rendered for this entry
    resolution = Column(String(20), nullable=True)
    resolution_value = Column(JSON, nullable=True)  # chip choice / typed text

    run = relationship("ClarifierRun", back_populates="detections")

    def __repr__(self) -> str:
        return f"<DetectionRecord run={self.run_id} {self.code}={self.result}>"
