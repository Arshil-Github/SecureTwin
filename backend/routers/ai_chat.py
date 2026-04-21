# backend/routers/ai_chat.py
from fastapi import APIRouter, Depends
from typing import List, Optional, Dict
from pydantic import BaseModel
from backend.services.ai_provider import ai_provider
from backend.services.prompts import SYSTEM_PROMPTS, build_prompt
from backend.services.wealth_mapper import WealthMapper
from backend.services.strategy_engine import StrategyEngine
from backend.schemas.action import WealthAction
import json

router = APIRouter()

# Mock Auth
async def get_current_user_id():
    return 1

class ChatMessage(BaseModel):
    role: str # user, assistant
    content: str

class ChatRequest(BaseModel):
    user_message: str
    conversation_history: List[ChatMessage] # last 6 messages
    user_id: int

class ChatResponse(BaseModel):
    assistant_message: str
    referenced_actions: Optional[List[WealthAction]] = None
    tokens_used: int

@router.post("/message", response_model=ChatResponse)
async def chat_message(req: ChatRequest):
    mapper = WealthMapper()
    strat = StrategyEngine()
    
    snapshot = await mapper.get_wealth_snapshot(req.user_id)
    actions = await strat.generate_wealth_actions(req.user_id)
    
    # Build a small context
    context = {
        "net_worth": snapshot.net_worth,
        "total_cash": snapshot.total_cash,
        "stress_score": snapshot.financial_stress_score,
        "top_actions": [a.title for a in actions[:2]]
    }
    
    prompt = build_prompt("chat_response", 
                          user_message=req.user_message, 
                          context_json=json.dumps(context))
    
    res = await ai_provider.complete(prompt, system=SYSTEM_PROMPTS["wealth_advisor"])
    
    return ChatResponse(
        assistant_message=res.text,
        referenced_actions=actions[:2], # Simplified
        tokens_used=res.tokens_used
    )

@router.get("/suggested-questions")
async def get_suggested_questions(user_id: int = Depends(get_current_user_id)):
    # Rule-based suggestions
    return [
        "How can I reduce my financial stress?",
        "Should I increase my SIPs?",
        "What is my net worth projection for 10 years?",
        "How can I build an emergency fund?",
        "Am I overspending on food?"
    ]

@router.post("/explain/{action_id}")
async def explain_action(action_id: str, user_id: int = Depends(get_current_user_id)):
    # Mock lookup
    description = "Move excess cash to liquid fund"
    prompt = build_prompt("explain_recommendation", action_description=description)
    res = await ai_provider.complete(prompt, system=SYSTEM_PROMPTS["wealth_advisor"])
    return {"explanation": res.text, "tokens_used": res.tokens_used}
