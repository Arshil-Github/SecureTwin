# backend/models/asset.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from backend.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_type = Column(String)  # property/gold/vehicle/other
    name = Column(String, nullable=False)
    purchase_value = Column(Float)
    current_value = Column(Float)
    purchase_date = Column(DateTime)
    notes = Column(String)
