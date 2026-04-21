# backend/schemas/investment.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InvestmentBase(BaseModel):
    account_type: Optional[str] = None
    folio_number: Optional[str] = None
    scheme_name: Optional[str] = None
    units_held: Optional[float] = None
    nav: Optional[float] = None
    current_value: Optional[float] = None
    invested_amount: Optional[float] = None
    sip_amount: Optional[float] = None
    sip_frequency: Optional[str] = None
    sip_date: Optional[int] = None
    start_date: Optional[datetime] = None
    last_transaction_date: Optional[datetime] = None
    returns_absolute: Optional[float] = None
    returns_xirr: Optional[float] = None
    maturity_date: Optional[datetime] = None
    interest_rate: Optional[float] = None
    principal: Optional[float] = None
    auto_renewal: bool = False

class InvestmentCreate(InvestmentBase):
    pass

class InvestmentRead(InvestmentBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
