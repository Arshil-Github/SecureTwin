# backend/services/strategy_engine.py
from typing import List, Optional
from pydantic import BaseModel
from backend.schemas.action import WealthAction
from backend.services.wealth_mapper import WealthMapper
from backend.services.behaviour_engine import BehaviourEngine
from backend.services.goal_engine import GoalEngine
from backend.services.spend_lens import SpendLens

class HabitROIResult(BaseModel):
    monthly_savings_freed: float
    yearly_savings_freed: float
    goal_acceleration: dict
    ten_year_wealth_impact: float
    message: str

class InsightsSummary(BaseModel):
    portfolio_health_score: int
    stress_score: int
    top_action: Optional[WealthAction]
    goal_summary: List[dict]

class StrategyEngine:
    
    async def generate_wealth_actions(self, user_id: int) -> List[WealthAction]:
        mapper = WealthMapper()
        be_engine = BehaviourEngine()
        goal_engine = GoalEngine()
        spend_lens = SpendLens()
        
        snapshot = await mapper.get_wealth_snapshot(user_id)
        profile = await be_engine.compute_behaviour_profile(user_id)
        stress = await be_engine.compute_financial_stress_score(user_id)
        goals = await goal_engine.get_all_goal_statuses(user_id)
        overspends = await spend_lens.detect_overspend(user_id)
        
        actions = []
        
        # RULE SET 1 - Cash Drag
        if snapshot.total_cash > 6 * 50000: # Assuming 50k monthly expense
            actions.append(WealthAction(
                action_id="cash_drag",
                title="Move excess cash to liquid fund",
                description="You have more than 6 months of expenses in cash. Move it to a liquid fund for better returns.",
                action_type="move_funds",
                impact_level="high",
                urgency="this_week",
                expected_impact_description="Earn 2-3% more than savings account."
            ))
            
        # RULE SET 5 - Goal at Risk
        for g in goals:
            if g.health.status == "at_risk":
                actions.append(WealthAction(
                    action_id=f"goal_risk_{g.id}",
                    title=f"Increase contribution to {g.name}",
                    description=f"Your {g.name} goal is at risk. Increase monthly contribution by ₹{g.health.gap_amount:,.0f}.",
                    action_type="increase_sip",
                    impact_level="high",
                    urgency="this_week",
                    expected_impact_description="Brings goal back on track.",
                    goal_impact_score=0.9
                ))

        # RULE SET 6 - No Emergency Fund
        if not any(g.name.lower() == "emergency fund" for g in goals):
            actions.append(WealthAction(
                action_id="emergency_fund",
                title="Build an emergency buffer",
                description="You don't have an emergency fund goal. Start by saving 3 months of expenses.",
                action_type="alert",
                impact_level="high",
                urgency="immediate",
                expected_impact_description="Provides financial security."
            ))
            
        # Sort by urgency and impact
        urgency_map = {"immediate": 0, "this_week": 1, "this_month": 2}
        impact_map = {"high": 0, "medium": 1, "low": 2}
        
        actions.sort(key=lambda x: (urgency_map[x.urgency], impact_map[x.impact_level]))
        
        return actions[:5]

    async def quantify_habit_roi(self, user_id: int, category: str, reduction_pct: float) -> HabitROIResult:
        spend_lens = SpendLens()
        summary = await spend_lens.get_spend_summary(user_id)
        
        cat_spend = summary.by_category.get(category, 0)
        freed = cat_spend * (reduction_pct / 100)
        
        return HabitROIResult(
            monthly_savings_freed=freed,
            yearly_savings_freed=freed * 12,
            goal_acceleration={},
            ten_year_wealth_impact=freed * 12 * 10 * 1.5, # Simplified compounding
            message=f"Cutting {category} by {reduction_pct}% frees ₹{freed:,.0f}/month."
        )
