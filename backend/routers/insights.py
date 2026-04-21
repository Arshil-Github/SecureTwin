# backend/routers/insights.py
from fastapi import APIRouter, Depends
from typing import List
from backend.services.strategy_engine import StrategyEngine, HabitROIResult, InsightsSummary
from backend.schemas.action import WealthAction
from backend.services.wealth_mapper import WealthMapper
from backend.services.behaviour_engine import BehaviourEngine
from backend.services.goal_engine import GoalEngine

router = APIRouter()

# Mock Auth
async def get_current_user_id():
    return 1

@router.get("/actions", response_model=List[WealthAction])
async def get_actions(user_id: int = Depends(get_current_user_id)):
    engine = StrategyEngine()
    return await engine.generate_wealth_actions(user_id)

@router.get("/habit-roi/{category}")
async def get_habit_roi(
    category: str, 
    reduction_pct: float = 30,
    user_id: int = Depends(get_current_user_id)
):
    engine = StrategyEngine()
    return await engine.quantify_habit_roi(user_id, category, reduction_pct)

@router.get("/summary", response_model=InsightsSummary)
async def get_summary(user_id: int = Depends(get_current_user_id)):
    mapper = WealthMapper()
    be_engine = BehaviourEngine()
    goal_engine = GoalEngine()
    strat_engine = StrategyEngine()
    
    snapshot = await mapper.get_wealth_snapshot(user_id)
    stress = await be_engine.compute_financial_stress_score(user_id)
    actions = await strat_engine.generate_wealth_actions(user_id)
    goals = await goal_engine.get_all_goal_statuses(user_id)
    
    return InsightsSummary(
        portfolio_health_score=snapshot.portfolio_health_score,
        stress_score=stress.score,
        top_action=actions[0] if actions else None,
        goal_summary=[{"name": g.name, "status": g.health.status, "pct_complete": (g.health.current_amount/g.health.target_amount)*100} for g in goals]
    )
