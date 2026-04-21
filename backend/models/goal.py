# backend/models/goal.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from backend.database import Base
import enum

class GoalType(str, enum.Enum):
    time_bound = "time_bound"
    amount_bound = "amount_bound"
    habit_bound = "habit_bound"

class GoalHealthStatus(str, enum.Enum):
    on_track = "on_track"
    at_risk = "at_risk"
    off_track = "off_track"

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    goal_type = Column(Enum(GoalType))
    target_amount = Column(Float)
    target_date = Column(DateTime)
    current_amount = Column(Float, default=0.0)
    monthly_contribution = Column(Float, default=0.0)
    health_status = Column(Enum(GoalHealthStatus), default=GoalHealthStatus.on_track)
    priority = Column(Integer, default=3) # 1-5
    created_at = Column(DateTime(timezone=True), server_default=func.now())
