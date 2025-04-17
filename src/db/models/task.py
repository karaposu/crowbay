# models/task.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base, get_current_time

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    desc = Column(String, nullable=False)
    total_budget = Column(Float, default=0.0)
    you_earn = Column(Float, default=0.0)
    status = Column(String, default="open")  # e.g., "open", "accepted", "completed", "disputed"
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    partition_deadline = Column(DateTime(timezone=True), nullable=True)
    submission_deadline = Column(DateTime(timezone=True), nullable=True)
    category = Column(String, nullable=True)
    bay_review = Column(Boolean, default=False)
    
    # Relationship back to the user who created the task
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task id={self.id} desc={self.desc} status={self.status}>"
