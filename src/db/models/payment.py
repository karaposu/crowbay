# models/payment.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
# from ..database import Base
from .base import Base, get_current_time

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    coin_ticker = Column(String, nullable=False, default="USDT")  # e.g., "USDT", "PEPE"
    amount = Column(Float, default=0.0)
    payment_type = Column(String, nullable=False)  # e.g., "deposit", "withdraw"
    status = Column(String, default="pending")     # e.g., "pending", "transaction_started", "completed", "failed"
    transfer_id = Column(String, nullable=True)    # TX reference if needed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="payments")
    # Optionally link a payment to a task (e.g., if it's paying for a task):
    task = relationship("Task", backref="payments")  # You can remove if not needed

    def __repr__(self):
        return f"<Payment id={self.id} user_id={self.user_id} type={self.payment_type} status={self.status}>"
    