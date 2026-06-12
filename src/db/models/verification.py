# filepath: src/db/models/verification.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Float, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from db.models.base import Base


class ProofType(Base):
    """Defines what types of proofs can be uploaded"""
    __tablename__ = "proof_types"

    id = Column(Integer, primary_key=True, index=True)
    proof_name = Column(String(100), unique=True, nullable=False)  # e.g., "government_id_photo", "selfie_video"
    proof_category = Column(String(50), nullable=False)  # e.g., "document", "biometric", "credential"
    description = Column(Text, nullable=False)
    file_requirements = Column(JSON, nullable=False)  # accepted formats, size limits, etc.
    extraction_capabilities = Column(JSON, nullable=False)  # what data can be extracted
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    verification_requirements = relationship("VerificationProofRequirement", back_populates="proof_type")
    user_proofs = relationship("UserProof", back_populates="proof_type")


class VerificationType(Base):
    """Defines what needs to be verified"""
    __tablename__ = "verification_types"

    id = Column(Integer, primary_key=True, index=True)
    verification_name = Column(String(100), unique=True, nullable=False)  # e.g., "age_verification", "identity_verification"
    tier = Column(Integer, nullable=False, index=True)  # 0-5
    description = Column(Text, nullable=False)
    expires_after_days = Column(Integer, nullable=True)  # NULL for permanent
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    proof_requirements = relationship("VerificationProofRequirement", back_populates="verification_type")
    user_verifications = relationship("UserVerification", back_populates="verification_type")


class VerificationProofRequirement(Base):
    """Links verifications to required proofs"""
    __tablename__ = "verification_proof_requirements"

    id = Column(Integer, primary_key=True, index=True)
    verification_type_id = Column(Integer, ForeignKey("verification_types.id"), nullable=False)
    proof_type_id = Column(Integer, ForeignKey("proof_types.id"), nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    alternative_group = Column(Integer, nullable=True)  # NULL or group number for "OR" requirements
    validation_rules = Column(JSON, nullable=True)  # specific rules for this proof in this verification
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    verification_type = relationship("VerificationType", back_populates="proof_requirements")
    proof_type = relationship("ProofType", back_populates="verification_requirements")


class UserProof(Base):
    """Actual uploaded proofs from users"""
    __tablename__ = "user_proofs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    proof_type_id = Column(Integer, ForeignKey("proof_types.id"), nullable=False)
    status = Column(String(20), nullable=False, default="uploaded")  # uploaded, processing, verified, rejected
    file_path = Column(String(500), nullable=False)  # encrypted path
    file_hash = Column(String(64), nullable=False)  # SHA-256 hash
    extracted_data = Column(JSON, nullable=True)  # AI-extracted information
    quality_score = Column(Float, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="proofs")
    proof_type = relationship("ProofType", back_populates="user_proofs")
    verification_usages = relationship("VerificationProofUsage", back_populates="user_proof")


class UserVerification(Base):
    """Tracks which verifications users have completed"""
    __tablename__ = "user_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    verification_type_id = Column(Integer, ForeignKey("verification_types.id"), nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending, verified, rejected, expired
    completed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="verifications")
    verification_type = relationship("VerificationType", back_populates="user_verifications")
    proof_usages = relationship("VerificationProofUsage", back_populates="user_verification")
    extracted_data = relationship("VerificationData", back_populates="source_verification")
    history = relationship("VerificationHistory", back_populates="user_verification")


class VerificationProofUsage(Base):
    """Links user proofs to verifications"""
    __tablename__ = "verification_proof_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_verification_id = Column(Integer, ForeignKey("user_verifications.id"), nullable=False)
    user_proof_id = Column(Integer, ForeignKey("user_proofs.id"), nullable=False)
    validation_result = Column(JSON, nullable=True)  # Results of validation for this specific usage
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
   
    # Relationships
    user_verification = relationship("UserVerification", back_populates="proof_usages")
    user_proof = relationship("UserProof", back_populates="verification_usages")


class VerificationData(Base):
    """Extracted/verified information stored in searchable format"""
    __tablename__ = "verification_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    field_name = Column(String(50), nullable=False, index=True)  # e.g., "birth_date", "gender", "education_level"
    field_value = Column(Text, nullable=False)  # Will be encrypted in production
    verification_source_id = Column(Integer, ForeignKey("user_verifications.id"), nullable=False)
    confidence_score = Column(Float, nullable=True)
    is_current = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="verification_data")
    source_verification = relationship("UserVerification", back_populates="extracted_data")

    # Indexes for common queries
    __table_args__ = (
        # Index for finding all current data for a user
        Index('idx_user_current_data', 'user_id', 'is_current'),
        # Index for searching by field name and value
        Index('idx_field_search', 'field_name', 'field_value'),
    )


class VerificationHistory(Base):
    """Audit trail for all verification actions"""
    __tablename__ = "verification_history"

    id = Column(Integer, primary_key=True, index=True)
    user_verification_id = Column(Integer, ForeignKey("user_verifications.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False)  # submitted, approved, rejected, expired, updated
    actor_id = Column(String(50), nullable=False)  # "system" or user ID
    actor_type = Column(String(20), nullable=False, default="system")  # "system", "user", "admin"
    action_details = Column(JSON, nullable=True)  # Additional context about the action
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user_verification = relationship("UserVerification", back_populates="history")

    # Index for chronological queries
    __table_args__ = (
        Index('idx_verification_history_chronological', 'user_verification_id', 'created_at'),
    )