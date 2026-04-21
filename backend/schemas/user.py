# backend/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from backend.models.user import RiskAppetite

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    age: Optional[int] = None
    monthly_income: Optional[int] = None
    risk_appetite: RiskAppetite = RiskAppetite.moderate

class UserCreate(UserBase):
    password: str
    device_fingerprint: Optional[str] = None

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_kyc_verified: Optional[bool] = None
    pan_number: Optional[str] = None

class UserRead(UserBase):
    id: int
    is_kyc_verified: bool
    created_at: datetime
    trusted_devices: List[str]

    class Config:
        from_attributes = True
