# backend/models/audit_log.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from backend.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(String)
    entity_type = Column(String)
    entity_id = Column(Integer)
    payload = Column(JSON)
    fraud_check_result = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
