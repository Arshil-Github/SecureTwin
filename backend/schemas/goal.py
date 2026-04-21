# backend/schemas/goal.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from backend.models.goal import GoalType, GoalHealthStatus

class GoalBase(BaseModel):
    name: str
    goal_type: Optional[GoalType] = None
    target_amount: Optional[float] = None
    target_date: Optional[datetime] = None
    current_amount: float = 0.0
    monthly_contribution: float = 0.0
    health_status: GoalHealthStatus = GoalHealthStatus.on_track
    priority: int = 3

class GoalCreate(GoalBase):
    pass

class GoalRead(GoalBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
