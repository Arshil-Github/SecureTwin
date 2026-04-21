# backend/schemas/action.py
from pydantic import BaseModel
from typing import Optional, Any, Literal

class WealthAction(BaseModel):
    action_id: str
    title: str
    description: str
    action_type: Literal["move_funds", "rebalance", "reduce_spend", "increase_sip", "tax_save", "alert"]
    impact_level: Literal["high", "medium", "low"]
    urgency: Literal["immediate", "this_week", "this_month"]
    expected_impact_description: str
    goal_impact_score: Optional[float] = None
    data_payload: Optional[dict] = None # JSON for frontend deep-linking
