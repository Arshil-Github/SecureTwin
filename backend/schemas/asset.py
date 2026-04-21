# backend/schemas/asset.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AssetBase(BaseModel):
    asset_type: Optional[str] = None
    name: str
    purchase_value: Optional[float] = None
    current_value: Optional[float] = None
    purchase_date: Optional[datetime] = None
    notes: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetRead(AssetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
