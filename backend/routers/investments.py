# backend/routers/investments.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import select
from backend.database import get_db, AsyncSessionLocal
from backend.models.investment import Investment
from backend.schemas.investment import InvestmentRead, InvestmentCreate
from backend.fraud.hooks import run_full_fraud_check
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Mock Auth
async def get_current_user_id():
    return 1

@router.get("/", response_model=List[InvestmentRead])
async def get_investments(user_id: int = Depends(get_current_user_id)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Investment).where(Investment.user_id == user_id))
        return result.scalars().all()

@router.post("/", response_model=InvestmentRead)
async def add_investment(
    inv_in: InvestmentCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    # FRAUD_HOOK
    run_full_fraud_check(user_id, {"action": "add_investment", "scheme": inv_in.scheme_name})
    
    inv = Investment(**inv_in.model_dump(), user_id=user_id)
    db.add(inv)
    await db.commit()
    await db.refresh(inv)
    return inv
