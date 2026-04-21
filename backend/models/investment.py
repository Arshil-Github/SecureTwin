# backend/models/investment.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from backend.database import Base

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_type = Column(String)  # mutual_fund/fd/rd/savings/stocks
    folio_number = Column(String)
    scheme_name = Column(String)
    units_held = Column(Float)
    nav = Column(Float)
    current_value = Column(Float)
    invested_amount = Column(Float)
    sip_amount = Column(Float)
    sip_frequency = Column(String)
    sip_date = Column(Integer)
    start_date = Column(DateTime)
    last_transaction_date = Column(DateTime)
    returns_absolute = Column(Float)
    returns_xirr = Column(Float)
    maturity_date = Column(DateTime)
    interest_rate = Column(Float)
    principal = Column(Float)
    auto_renewal = Column(Boolean, default=False)
