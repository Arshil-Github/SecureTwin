# backend/routers/goals.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import select
from backend.database import get_db, AsyncSessionLocal
from backend.models.goal import Goal, GoalHealthStatus
from backend.models.user import User
from backend.schemas.goal import GoalRead, GoalCreate
from backend.services.goal_engine import GoalEngine, GoalStatus, GoalConflict
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Mock Auth
async def get_current_user_id():
    return 1

@router.get("/", response_model=List[GoalStatus])
async def get_goals(user_id: int = Depends(get_current_user_id)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Goal).where(Goal.user_id == user_id))
        goals = result.scalars().all()
        
        engine = GoalEngine()
        statuses = []
        for g in goals:
            health = engine.get_goal_health(g, 0)
            statuses.append(GoalStatus(id=g.id, name=g.name, health=health))
        return statuses

@router.post("/", response_model=GoalRead)
async def create_goal(
    goal_in: GoalCreate, 
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    # FRAUD_HOOK
    from backend.fraud.hooks import run_full_fraud_check
    run_full_fraud_check(user_id, {"action": "create_goal", "name": goal_in.name})
    
    goal = Goal(**goal_in.model_dump(), user_id=user_id)
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal

@router.get("/conflicts", response_model=List[GoalConflict])
async def get_goal_conflicts(user_id: int = Depends(get_current_user_id)):
    async with AsyncSessionLocal() as session:
        # Get goals and user income
        res_goals = await session.execute(select(Goal).where(Goal.user_id == user_id))
        goals = res_goals.scalars().all()
        
        res_user = await session.execute(select(User).where(User.id == user_id))
        user = res_user.scalars().first()
        
        engine = GoalEngine()
        return engine.detect_goal_conflicts(user_id, goals, user.monthly_income if user else 0)

@router.get("/{goal_id}/impact/{action_type}")
async def get_goal_impact(
    goal_id: int, 
    action_type: str, 
    amount: float = 5000,
    user_id: int = Depends(get_current_user_id)
):
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id))
        goal = res.scalars().first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        engine = GoalEngine()
        return engine.compute_goal_impact_score(action_type, amount, goal)
