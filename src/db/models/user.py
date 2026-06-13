# filepath: src/db/models/user.py

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base, utcnow


class User(Base):
    """One account can act as both Launcher and Jumper; role is per-action.

    Demographic facts deliberately do NOT live here — they live in
    verification_data as verified attributes.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    # Both nullable: accounts created through the Telegram bridge have a
    # telegram_id but no email/password. Code must ensure every account has
    # at least one sign-in method (email+password or telegram_id).
    email = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(String(128), nullable=True)
    name = Column(String(100), nullable=True)
    telegram_handle = Column(String(64), nullable=True)
    telegram_id = Column(String(64), nullable=True, index=True)
    is_email_verified = Column(Boolean, nullable=False, default=False)
    # Written only on successful OTP verify — a set phone is a verified phone.
    phone_number = Column(String(20), unique=True, nullable=True, index=True)
    phone_verified_at = Column(DateTime(timezone=True), nullable=True)
    notifications_muted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    tasks = relationship("Task", back_populates="owner")
    jumps = relationship("Jump", back_populates="jumper")
    payments = relationship("Payment", back_populates="user")
    proofs = relationship("UserProof", back_populates="user")
    verifications = relationship("UserVerification", back_populates="user")
    verification_data = relationship("VerificationData", back_populates="user")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
