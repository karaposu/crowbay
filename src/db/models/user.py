# here is db/models/user.py

from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Float, Text,
    ForeignKey, LargeBinary, Boolean, UniqueConstraint, CheckConstraint, or_, func
)
from sqlalchemy.types import JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash

from .base import Base, get_current_time


# we need also table related to all verifications. we cant store everyhing at in user table 

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    telegram_handler = Column(String(50), nullable=True)
    telegram_id = Column(String(50), nullable=True)
    gender = Column(String(50), nullable=True)
    nationality = Column(String(50), nullable=True)
    birthyear = Column(String(50), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=get_current_time)
    
    is_eamil_verified = Column(Boolean, default=False)
    is_id_verified = Column(Boolean, default=False)
    does_id_photo_and_selfie_match = Column(Boolean, default=False)


    # 1) Relationship for Payment
    payments = relationship("Payment",
                            back_populates="user",
                            cascade="all, delete-orphan")

    # 2) Relationship for Task
    tasks = relationship("Task",
                         back_populates="owner",
                         cascade="all, delete-orphan")
    

    validations = relationship(
        "BaseUserValidation",
        back_populates="user",
        cascade="all, delete-orphan"
    )
  

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"





