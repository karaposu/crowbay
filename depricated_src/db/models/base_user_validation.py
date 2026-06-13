# db/models/base_user_validation.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship

from .base import Base, get_current_time

class BaseUserValidation(Base):
    """
    Stores detailed user identity verification data separate from the main user table.
    This can include ID document paths, selfies, statuses, and more.
    """
    __tablename__ = "base_user_validation"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Link back to the user table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Paths or references to uploaded images/documents
    id_document_path = Column(String(255), nullable=True)
    selfie_path = Column(String(255), nullable=True)
    
    selfie_extracted_face = Column(String(255), nullable=True)
    extracted_birthday = Column(String(255), nullable=True)
    extracted_image = Column(String(255), nullable=True)
    
    # Timestamps for creation and verification
    created_at = Column(DateTime, default=get_current_time)
    verified_at = Column(DateTime, nullable=True)
    
    verified_by = Column(String(255), nullable=True)

    # Verification status ("pending", "approved", "rejected", etc.)
    status = Column(String(50), default="pending", nullable=False)

    # Store any reason or notes (e.g., if rejected)
    rejection_reason = Column(String(255), nullable=True)

    # Relationship back to the User object
    user = relationship("User", back_populates="validations")

    def __repr__(self):
        return f"<BaseUserValidation id={self.id} user_id={self.user_id} status={self.status}>"
