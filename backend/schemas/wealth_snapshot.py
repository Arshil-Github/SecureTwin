# backend/schemas/wealth_snapshot.py
from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from .investment import InvestmentRead
from .asset import AssetRead

class WealthSnapshot(BaseModel):
    user_id: int
    snapshot_date: date
    total_cash: float
    total_investments: float
    total_assets: float
    total_liabilities: float
    net_worth: float
    net_worth_delta_mom: float # month-on-month change
    portfolio_health_score: float # 0-100
    financial_stress_score: float # 0-100
    investments: List[InvestmentRead]
    assets: List[AssetRead]
