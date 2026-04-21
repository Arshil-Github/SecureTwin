# backend/routers/transactions.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy import select, func
from backend.database import AsyncSessionLocal, get_db
from backend.models.transaction import Transaction, TransactionCategory
from backend.schemas.transaction import TransactionRead, TransactionCreate
from backend.services.transaction_ingestor import TransactionIngestor, IngestResult
from backend.services.spend_lens import SpendLens, SpendSummary, CategorySummary, OverspendAlert
from backend.fraud.hooks import run_full_fraud_check
from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.behaviour_engine import BehaviourEngine, BehaviourProfile, StressScoreResult, AnomalyAlert, BehaviourInsight

router = APIRouter()

# Mock Auth Dependency
async def get_current_user_id():
    return 1 # Default to Priya for hackathon demo

@router.get("/behaviour/profile", response_model=BehaviourProfile)
async def get_behaviour_profile(user_id: int = Depends(get_current_user_id)):
    engine = BehaviourEngine()
    return await engine.compute_behaviour_profile(user_id)

@router.get("/behaviour/stress-score", response_model=StressScoreResult)
async def get_stress_score(user_id: int = Depends(get_current_user_id)):
    engine = BehaviourEngine()
    return await engine.compute_financial_stress_score(user_id)

@router.get("/behaviour/anomalies", response_model=List[AnomalyAlert])
async def get_anomalies(user_id: int = Depends(get_current_user_id)):
    engine = BehaviourEngine()
    return await engine.detect_anomalies(user_id)

@router.get("/behaviour/insights", response_model=List[BehaviourInsight])
async def get_insights(user_id: int = Depends(get_current_user_id)):
    engine = BehaviourEngine()
    return await engine.get_behaviour_insights(user_id)

@router.post("/ingest", response_model=IngestResult)
async def ingest_transactions(
    raw_txns: List[dict], 
    source: str = "manual",
    user_id: int = Depends(get_current_user_id)
):
    ingestor = TransactionIngestor()
    return await ingestor.ingest(raw_txns, user_id, source)

@router.get("/summary", response_model=SpendSummary)
async def get_spend_summary(
    period_days: int = 30,
    user_id: int = Depends(get_current_user_id)
):
    lens = SpendLens()
    return await lens.get_spend_summary(user_id, period_days)

@router.get("/category/{category}", response_model=CategorySummary)
async def get_category_summary(
    category: str,
    period_days: int = 30,
    user_id: int = Depends(get_current_user_id)
):
    lens = SpendLens()
    return await lens.get_category_summary(user_id, category, period_days)

@router.get("/overspend", response_model=List[OverspendAlert])
async def get_overspend_alerts(
    user_id: int = Depends(get_current_user_id)
):
    lens = SpendLens()
    return await lens.detect_overspend(user_id)

@router.get("/list", response_model=List[TransactionRead])
async def list_transactions(
    limit: int = 50,
    offset: int = 0,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()

@router.put("/{txn_id}/category", response_model=TransactionRead)
async def recategorize_transaction(
    txn_id: int,
    new_category: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    # FRAUD_HOOK
    run_full_fraud_check(user_id, {"action": "recategorize", "txn_id": txn_id})
    
    result = await db.execute(select(Transaction).where(Transaction.id == txn_id, Transaction.user_id == user_id))
    txn = result.scalars().first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    txn.category = TransactionCategory(new_category)
    await db.commit()
    await db.refresh(txn)
    return txn
