# backend/schemas/transaction.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from backend.models.transaction import TransactionCategory

class TransactionBase(BaseModel):
    amount: float
    type: str # debit/credit
    merchant_raw: Optional[str] = None
    merchant_normalized: Optional[str] = None
    category: TransactionCategory = TransactionCategory.OTHER
    sub_category: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None
    is_recurring: bool = False
    spending_personality_tag: Optional[str] = None

class TransactionCreate(TransactionBase):
    txn_id: str
    timestamp: Optional[datetime] = None

class TransactionRead(TransactionBase):
    id: int
    user_id: int
    txn_id: str
    timestamp: datetime
    balance_after: Optional[float] = None

    class Config:
        from_attributes = True
