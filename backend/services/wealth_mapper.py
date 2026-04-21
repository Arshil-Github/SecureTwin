# backend/services/wealth_mapper.py
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel
from sqlalchemy import select
from backend.database import AsyncSessionLocal
from backend.models.investment import Investment
from backend.models.asset import Asset
from backend.models.transaction import Transaction
from backend.schemas.wealth_snapshot import WealthSnapshot
from backend.services.behaviour_engine import BehaviourEngine
from backend.utils.xirr import xirr

class InvestmentSummary(BaseModel):
    total_invested: float
    current_value: float
    absolute_return_pct: float
    xirr_overall: Optional[float]
    underperforming_flags: List[str]

class WealthMapper:
    
    async def get_wealth_snapshot(self, user_id: int) -> WealthSnapshot:
        async with AsyncSessionLocal() as session:
            # 1. Get Investments
            res_inv = await session.execute(select(Investment).where(Investment.user_id == user_id))
            investments = res_inv.scalars().all()
            
            # 2. Get Assets
            res_asset = await session.execute(select(Asset).where(Asset.user_id == user_id))
            assets = res_asset.scalars().all()
            
            # 3. Get Cash (from last transaction balance)
            res_cash = await session.execute(
                select(Transaction.balance_after)
                .where(Transaction.user_id == user_id)
                .order_by(Transaction.timestamp.desc())
                .limit(1)
            )
            total_cash = res_cash.scalar() or 0.0
            
            total_investments = sum(i.current_value for i in investments)
            total_assets = sum(a.current_value for a in assets)
            net_worth = total_cash + total_investments + total_assets
            
            # Behaviour Score
            be_engine = BehaviourEngine()
            stress_res = await be_engine.compute_financial_stress_score(user_id)
            
            return WealthSnapshot(
                user_id=user_id,
                snapshot_date=datetime.now().date(),
                total_cash=total_cash,
                total_investments=total_investments,
                total_assets=total_assets,
                total_liabilities=0.0,
                net_worth=net_worth,
                net_worth_delta_mom=0.0, # MoM logic simplified
                portfolio_health_score=self._compute_portfolio_health(investments, total_cash),
                financial_stress_score=stress_res.score,
                investments=[self._to_schema(i) for i in investments],
                assets=[self._to_schema_asset(a) for a in assets]
            )

    def _compute_portfolio_health(self, investments: List[Investment], total_cash: float) -> int:
        score = 0
        
        # Diversification (30pts)
        types = set(i.account_type for i in investments)
        if len(types) >= 3: score += 30
        elif len(types) == 2: score += 20
        elif len(types) == 1: score += 10
        
        # Return quality (30pts) - Simplified
        avg_xirr = sum(i.returns_xirr for i in investments if i.returns_xirr) / len(investments) if investments else 0
        if avg_xirr > 0.12: score += 30
        elif avg_xirr > 0.08: score += 20
        elif avg_xirr > 0.04: score += 10
        
        # Emergency buffer (20pts) - Assuming 50k monthly expense
        if total_cash > 150000: score += 20
        elif total_cash > 50000: score += 10
        
        return min(score, 100)

    def _to_schema(self, i: Investment):
        from backend.schemas.investment import InvestmentRead
        return InvestmentRead.model_validate(i, from_attributes=True)

    def _to_schema_asset(self, a: Asset):
        from backend.schemas.asset import AssetRead
        return AssetRead.model_validate(a, from_attributes=True)

    async def get_investment_summary(self, user_id: int) -> InvestmentSummary:
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(Investment).where(Investment.user_id == user_id))
            investments = res.scalars().all()
            
            total_invested = sum(i.invested_amount for i in investments)
            current_value = sum(i.current_value for i in investments)
            
            flags = []
            for i in investments:
                if i.account_type == 'fd' and i.interest_rate and i.interest_rate < 6.5:
                    flags.append(f"{i.scheme_name}: Rate below repo rate (6.5%)")
            
            return InvestmentSummary(
                total_invested=total_invested,
                current_value=current_value,
                absolute_return_pct=(current_value - total_invested) / total_invested if total_invested > 0 else 0,
                xirr_overall=None, # Simplified
                underperforming_flags=flags
            )
