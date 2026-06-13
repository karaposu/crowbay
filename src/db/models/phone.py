# filepath: src/db/models/phone.py

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String

from db.base import Base, utcnow


class SmsVerification(Base):
    """One OTP challenge. The phone number lands on users.phone_number only
    after a successful verify — pending requests never reserve a number."""

    __tablename__ = "sms_verifications"
    __table_args__ = (Index("ix_sms_verifications_user_created", "user_id", "created_at"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)
    code_hash = Column(String(64), nullable=False)  # sha256 of the 6-digit code
    attempts = Column(Integer, nullable=False, default=0)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
