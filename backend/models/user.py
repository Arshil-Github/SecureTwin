# backend/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, Enum, JSON, DateTime
from sqlalchemy.sql import func
from backend.database import Base
import enum

class RiskAppetite(str, enum.Enum):
    conservative = "conservative"
    moderate = "moderate"
    aggressive = "aggressive"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    pan_number = Column(String)  # TODO: Encrypt this
    age = Column(Integer)
    monthly_income = Column(Integer)
    risk_appetite = Column(Enum(RiskAppetite), default=RiskAppetite.moderate)
    is_kyc_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    trusted_devices = Column(JSON, default=[]) # Array of device fingerprints
