# backend/services/insight_narrator.py
from typing import Optional
from pydantic import BaseModel
from backend.schemas.action import WealthAction
from backend.services.ai_provider import AIProvider

class WeeklySummary(BaseModel):
    headline: str
    body: str
    positive_note: str
    top_action_cta: str

class NarratorContext(BaseModel):
    template_key: str
    template_output: str
    raw_data: dict
    user_name: str
    user_risk_appetite: str

class InsightNarrator:
    
    TEMPLATES = {
        "overspend": "Your spending on {category} (₹{current:,.0f}) is {pct:.0f}% above your {period}-month average of ₹{average:,.0f}.",
        "goal_at_risk": "At your current savings rate, you'll reach your {goal_name} goal {months_late} months late (by {projected_date}).",
        "stress_score": "Your financial stress score is {level} ({score}/100). Main contributors: {top_signals_joined}.",
        "portfolio_health": "Your portfolio health is {score}/100.",
        "wealth_action": "{action_title}. {expected_impact_description}",
        "habit_roi": "Cutting {category} spend by {pct:.0f}% frees ₹{freed:,.0f}/month.",
    }

    def narrate(self, template_key: str, **kwargs) -> str:
        template = self.TEMPLATES.get(template_key)
        if not template:
            raise ValueError(f"Template {template_key} not found")
        return template.format(**kwargs)

    async def narrate_with_ai(self, context: NarratorContext, tone: str = "friendly") -> str:
        ai = AIProvider()
        prompt = f"""
        Rewrite the following financial insight in a {tone} tone. 
        Limit to 3 sentences max.
        Original: {context.template_output}
        User Risk Appetite: {context.user_risk_appetite}
        """
        res = await ai.complete(prompt, max_tokens=150)
        return res if res else context.template_output

    def narrate_weekly_summary(self, user_id: int) -> WeeklySummary:
        # Mock logic for demo
        return WeeklySummary(
            headline="You saved 18% this week!",
            body="Great job staying consistent with your spending categories.",
            positive_note="Your grocery spend was 10% lower than last week. Small wins add up!",
            top_action_cta="Review your upcoming SIPs"
        )
