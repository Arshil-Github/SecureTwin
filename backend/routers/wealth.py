# backend/routers/wealth.py
from fastapi import APIRouter, Depends
from typing import List
from backend.services.wealth_mapper import WealthMapper, InvestmentSummary
from backend.schemas.wealth_snapshot import WealthSnapshot
from backend.fraud.hooks import run_full_fraud_check

from backend.services.scenario_simulator import ScenarioSimulator, ScenarioInput, MultiScenarioResult, ScenarioResult

from backend.schemas.asset import AssetRead, AssetCreate
from backend.models.asset import Asset
from backend.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Mock Auth Dependency
async def get_current_user_id():
    return 1 # Default to Priya

@router.post("/assets", response_model=AssetRead)
async def add_asset(
    asset_in: AssetCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    # FRAUD_HOOK
    run_full_fraud_check(user_id, {"action": "add_asset", "name": asset_in.name})
    
    asset = Asset(**asset_in.model_dump(), user_id=user_id)
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset

@router.post("/simulate/single", response_model=ScenarioResult)
async def simulate_single(
    scenario: ScenarioInput,
    user_id: int = Depends(get_current_user_id)
):
    sim = ScenarioSimulator()
    return await sim.run_scenario(user_id, scenario)

@router.post("/simulate/multi", response_model=MultiScenarioResult)
async def simulate_multi(
    scenarios: List[ScenarioInput],
    user_id: int = Depends(get_current_user_id)
):
    sim = ScenarioSimulator()
    return await sim.run_multi_scenario(user_id, scenarios)

@router.get("/simulate/presets/{target_user_id}")
async def get_presets(target_user_id: int):
    # Hardcoded presets for demo
    return [
        {
            "name": "Increase SIP by ₹1,000",
            "adjustments": [{"type": "increase_sip", "amount": 1000}]
        },
        {
            "name": "Cut Dining by 30%",
            "adjustments": [{"type": "reduce_spend", "amount": 2000}]
        }
    ]

@router.get("/snapshot", response_model=WealthSnapshot)
async def get_snapshot(user_id: int = Depends(get_current_user_id)):
    mapper = WealthMapper()
    return await mapper.get_wealth_snapshot(user_id)

@router.get("/investments", response_model=InvestmentSummary)
async def get_investments(user_id: int = Depends(get_current_user_id)):
    mapper = WealthMapper()
    return await mapper.get_investment_summary(user_id)

@router.get("/portfolio-health")
async def get_portfolio_health(user_id: int = Depends(get_current_user_id)):
    mapper = WealthMapper()
    snapshot = await mapper.get_wealth_snapshot(user_id)
    return {"score": snapshot.portfolio_health_score, "breakdown": {}}
