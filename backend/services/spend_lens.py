# backend/services/spend_lens.py
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel
from sqlalchemy import select, func
from backend.database import AsyncSessionLocal
from backend.models.transaction import Transaction, TransactionCategory

class CategorySummary(BaseModel):
    category: str
    total_spend: float
    transaction_count: int
    avg_transaction: float
    sub_categories: Dict[str, float]
    personality_tag: Optional[str] = None

class OverspendAlert(BaseModel):
    category: str
    current_spend: float
    average_spend: float
    pct_over: float
    human_message: str

class SpendSummary(BaseModel):
    period_start: datetime
    period_end: datetime
    total_spend: float
    total_income: float
    savings_rate: float
    by_category: Dict[str, float]
    top_merchants: List[Dict]
    mom_comparison: Dict[str, float]

class SpendLens:
    
    async def get_spend_summary(self, user_id: int, period_days: int = 30) -> SpendSummary:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        prev_start_date = start_date - timedelta(days=period_days)
        
        async with AsyncSessionLocal() as session:
            # Current Period
            result = await session.execute(
                select(Transaction).where(
                    Transaction.user_id == user_id,
                    Transaction.timestamp >= start_date
                )
            )
            txns = result.scalars().all()
            
            # Previous Period (for MoM)
            result_prev = await session.execute(
                select(Transaction).where(
                    Transaction.user_id == user_id,
                    Transaction.timestamp >= prev_start_date,
                    Transaction.timestamp < start_date
                )
            )
            prev_txns = result_prev.scalars().all()
            
            total_spend = sum(t.amount for t in txns if t.type == 'debit')
            total_income = sum(t.amount for t in txns if t.type == 'credit')
            savings_rate = (total_income - total_spend) / total_income if total_income > 0 else 0
            
            by_category = {}
            for t in txns:
                if t.type == 'debit':
                    cat = t.category.value
                    by_category[cat] = by_category.get(cat, 0) + t.amount
            
            # Top Merchants
            merchants = {}
            for t in txns:
                if t.type == 'debit':
                    name = t.merchant_normalized or t.merchant_raw
                    merchants[name] = merchants.get(name, 0) + t.amount
            top_merchants = [{"merchant": k, "amount": v} for k, v in sorted(merchants.items(), key=lambda x: x[1], reverse=True)[:5]]
            
            # MoM Comparison
            prev_by_category = {}
            for t in prev_txns:
                if t.type == 'debit':
                    cat = t.category.value
                    prev_by_category[cat] = prev_by_category.get(cat, 0) + t.amount
            
            mom = {}
            for cat, amount in by_category.items():
                prev_amount = prev_by_category.get(cat, 0)
                if prev_amount > 0:
                    mom[cat] = (amount - prev_amount) / prev_amount
                else:
                    mom[cat] = 1.0 # 100% increase if no previous spend
                    
            return SpendSummary(
                period_start=start_date,
                period_end=end_date,
                total_spend=total_spend,
                total_income=total_income,
                savings_rate=savings_rate,
                by_category=by_category,
                top_merchants=top_merchants,
                mom_comparison=mom
            )

    async def get_category_summary(self, user_id: int, category: str, period_days: int = 30) -> CategorySummary:
        start_date = datetime.now() - timedelta(days=period_days)
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Transaction).where(
                    Transaction.user_id == user_id,
                    Transaction.category == category,
                    Transaction.timestamp >= start_date
                )
            )
            txns = result.scalars().all()
            
            total_spend = sum(t.amount for t in txns)
            count = len(txns)
            avg = total_spend / count if count > 0 else 0
            
            sub_cats = {}
            for t in txns:
                sc = t.sub_category or "Other"
                sub_cats[sc] = sub_cats.get(sc, 0) + t.amount
            
            personality_tag = txns[0].spending_personality_tag if txns else None
            
            return CategorySummary(
                category=category,
                total_spend=total_spend,
                transaction_count=count,
                avg_transaction=avg,
                sub_categories=sub_cats,
                personality_tag=personality_tag
            )

    async def detect_overspend(self, user_id: int) -> List[OverspendAlert]:
        # Last 30 days vs 3-month average
        start_30d = datetime.now() - timedelta(days=30)
        start_90d = datetime.now() - timedelta(days=90)
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Transaction).where(
                    Transaction.user_id == user_id,
                    Transaction.timestamp >= start_90d,
                    Transaction.type == 'debit'
                )
            )
            all_txns = result.scalars().all()
            
            current_txns = [t for t in all_txns if t.timestamp >= start_30d]
            
            categories = set(t.category for t in all_txns)
            alerts = []
            
            for cat in categories:
                cat_current = sum(t.amount for t in current_txns if t.category == cat)
                cat_total_90d = sum(t.amount for t in all_txns if t.category == cat)
                cat_avg_monthly = cat_total_90d / 3
                
                if cat_current > 1.2 * cat_avg_monthly and cat_avg_monthly > 0:
                    pct_over = (cat_current - cat_avg_monthly) / cat_avg_monthly
                    alerts.append(OverspendAlert(
                        category=cat.value,
                        current_spend=cat_current,
                        average_spend=cat_avg_monthly,
                        pct_over=pct_over,
                        human_message=f"You spent ₹{cat_current:,.0f} on {cat.value} this month — {pct_over:.0%} above your usual ₹{cat_avg_monthly:,.0f}"
                    ))
            return alerts
