# backend/models/transaction.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from backend.database import Base
import enum

class TransactionCategory(str, enum.Enum):
    FOOD = "FOOD"
    TRANSPORT = "TRANSPORT"
    SHOPPING = "SHOPPING"
    UTILITIES = "UTILITIES"
    ENTERTAINMENT = "ENTERTAINMENT"
    HEALTH = "HEALTH"
    EDUCATION = "EDUCATION"
    EMI = "EMI"
    INVESTMENT = "INVESTMENT"
    INCOME = "INCOME"
    TRANSFER = "TRANSFER"
    OTHER = "OTHER"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    txn_id = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String)  # debit/credit
    merchant_raw = Column(String)
    merchant_normalized = Column(String)
    category = Column(Enum(TransactionCategory), default=TransactionCategory.OTHER)
    sub_category = Column(String)
    source = Column(String)  # UPI/bank/manual
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    balance_after = Column(Float)
    description = Column(String)
    is_recurring = Column(Boolean, default=False)
    spending_personality_tag = Column(String)
