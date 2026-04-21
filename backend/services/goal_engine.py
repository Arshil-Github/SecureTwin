# backend/services/goal_engine.py
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel
from backend.models.goal import Goal, GoalHealthStatus
from backend.schemas.action import WealthAction

from backend.database import AsyncSessionLocal
from sqlalchemy import select

class GoalHealthResult(BaseModel):
    status: str # on_track, at_risk, off_track
    current_amount: float
    target_amount: float
    target_date: date
    months_remaining: int
    required_monthly: float
    current_monthly: float
    projected_completion_date: date
    gap_amount: float

class GoalConflict(BaseModel):
    conflicting_goals: List[str]
    shortfall: float
    message: str

class GoalStatus(BaseModel):
    id: int
    name: str
    health: GoalHealthResult

class GoalEngine:
    
    def get_goal_health(self, goal: Goal, monthly_savings: float) -> GoalHealthResult:
        today = date.today()
        target_date = goal.target_date.date()
        
        months_remaining = (target_date.year - today.year) * 12 + (target_date.month - today.month)
        months_remaining = max(months_remaining, 1)
        
        remaining_amount = max(goal.target_amount - goal.current_amount, 0)
        required_monthly = remaining_amount / months_remaining
        
        current_monthly = goal.monthly_contribution
        
        # Projected completion
        if current_monthly > 0:
            months_to_completion = remaining_amount / current_monthly
            projected_completion_date = today + timedelta(days=int(months_to_completion * 30))
        else:
            projected_completion_date = date(2099, 12, 31) # Far future
            
        gap_amount = max(required_monthly - current_monthly, 0)
        
        if current_monthly == 0:
            status = "off_track"
        elif projected_completion_date <= target_date:
            status = "on_track"
        elif (projected_completion_date - target_date).days <= 180: # 6 months
            status = "at_risk"
        else:
            status = "off_track"
            
        return GoalHealthResult(
            status=status,
            current_amount=goal.current_amount,
            target_amount=goal.target_amount,
            target_date=target_date,
            months_remaining=months_remaining,
            required_monthly=required_monthly,
            current_monthly=current_monthly,
            projected_completion_date=projected_completion_date,
            gap_amount=gap_amount
        )

    def detect_goal_conflicts(self, user_id: int, goals: List[Goal], monthly_income: float) -> List[GoalConflict]:
        if not goals:
            return []
            
        total_required = 0
        goal_names = []
        for g in goals:
            health = self.get_goal_health(g, 0) # monthly_savings not used here
            total_required += health.required_monthly
            goal_names.append(g.name)
            
        # available_monthly = monthly_income - fixed_expenses (est 40%) - current_savings
        available_monthly = monthly_income * 0.4 
        
        if total_required > available_monthly * 1.1:
            shortfall = total_required - available_monthly
            return [GoalConflict(
                conflicting_goals=goal_names,
                shortfall=shortfall,
                message=f"You need ₹{total_required:,.0f}/month for all goals but only ₹{available_monthly:,.0f} is estimated as available. Prioritize which matters most."
            )]
        return []

    def compute_goal_impact_score(self, action_type: str, action_amount: float, goal: Goal) -> dict:
        health = self.get_goal_health(goal, 0)
        
        if health.required_monthly <= 0:
            return {"score": 1.0, "message": f"Your {goal.name} goal is already funded!"}
            
        score = min(action_amount / health.required_monthly, 1.0)
        pct = score * 100
        
        msg = f"This action covers {pct:.0f}% of your {goal.name} goal's monthly requirement."
        if score > 0.8:
            msg += f" It moves your goal from {goal.health_status.value} towards On Track."
            
        return {"score": score, "message": msg}

    async def get_all_goal_statuses(self, user_id: int) -> List[GoalStatus]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Goal).where(Goal.user_id == user_id))
            goals = result.scalars().all()
            
            statuses = []
            for g in goals:
                health = self.get_goal_health(g, 0)
                statuses.append(GoalStatus(id=g.id, name=g.name, health=health))
            return statuses

from datetime import timedelta
