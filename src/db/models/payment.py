# filepath: src/db/models/payment.py

import enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base, utcnow


class PaymentType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    ESCROW_HOLD = "escrow_hold"
    PAYOUT = "payout"
    COMMISSION = "commission"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Payment(Base):
    """Ledger row. Escrow logic belongs to the payments component; the table
    lands in the backbone so foreign keys and the ledger shape exist."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True, index=True)

    payment_type = Column(String(20), nullable=False)
    coin_ticker = Column(String(10), nullable=False, default="USDT")
    amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default=PaymentStatus.PENDING.value, index=True)
    tx_ref = Column(String(128), nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    user = relationship("User", back_populates="payments")
    task = relationship("Task")

    def __repr__(self) -> str:
        return f"<Payment id={self.id} {self.payment_type} {self.amount} {self.status}>"
