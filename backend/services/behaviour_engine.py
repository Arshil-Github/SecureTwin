# backend/services/behaviour_engine.py
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel
from sqlalchemy import select
from sklearn.ensemble import IsolationForest
from backend.database import AsyncSessionLocal
from backend.models.transaction import Transaction, TransactionCategory

class MonthSpendPattern(BaseModel):
    month_start_7d_avg: float
    month_end_7d_avg: float
    ratio: float

class BehaviourProfile(BaseModel):
    spend_to_income_ratio: Dict[str, float]
    weekend_vs_weekday_spend: float
    month_start_vs_end_spend: MonthSpendPattern
    recurring_vs_discretionary_ratio: float
    savings_rate_trend: List[float]
    impulse_spend_count: int
    top_spending_personality: Optional[str]

class StressScoreResult(BaseModel):
    score: int
    level: str # low, moderate, high, critical
    top_signals: List[str]
    trend: str # improving, stable, worsening

class AnomalyAlert(BaseModel):
    txn_id: str
    amount: float
    merchant: str
    reason: str
    anomaly_score: float

class BehaviourInsight(BaseModel):
    title: str
    observation: str
    impact: str

class BehaviourEngine:
    
    async def compute_behaviour_profile(self, user_id: int) -> BehaviourProfile:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Transaction).where(Transaction.user_id == user_id)
            )
            all_txns = result.scalars().all()
            
            # Weekend vs Weekday
            weekends = [t.amount for t in all_txns if t.timestamp.weekday() >= 5 and t.type == 'debit']
            weekdays = [t.amount for t in all_txns if t.timestamp.weekday() < 5 and t.type == 'debit']
            weekend_avg = np.mean(weekends) if weekends else 0
            weekday_avg = np.mean(weekdays) if weekdays else 0
            
            # Month Start vs End (Stress Indicator)
            start_7d = [t.amount for t in all_txns if t.timestamp.day <= 7 and t.type == 'debit']
            end_7d = [t.amount for t in all_txns if t.timestamp.day > 23 and t.type == 'debit']
            start_avg = np.mean(start_7d) if start_7d else 0
            end_avg = np.mean(end_7d) if end_7d else 0
            
            # Impulse Spend (2x category avg)
            cat_avgs = {}
            for t in all_txns:
                if t.type == 'debit':
                    cat_avgs.setdefault(t.category, []).append(t.amount)
            cat_avgs = {k: np.mean(v) for k, v in cat_avgs.items()}
            
            impulse_count = 0
            last_30d = [t for t in all_txns if t.timestamp > datetime.now() - timedelta(days=30)]
            for t in last_30d:
                if t.type == 'debit' and t.amount > 2 * cat_avgs.get(t.category, 0):
                    impulse_count += 1
            
            # Personality
            personalities = [t.spending_personality_tag for t in all_txns if t.spending_personality_tag]
            top_personality = max(set(personalities), key=personalities.count) if personalities else None

            return BehaviourProfile(
                spend_to_income_ratio={}, # Placeholder
                weekend_vs_weekday_spend=weekend_avg / weekday_avg if weekday_avg > 0 else 0,
                month_start_vs_end_spend=MonthSpendPattern(
                    month_start_7d_avg=start_avg,
                    month_end_7d_avg=end_avg,
                    ratio=end_avg / start_avg if start_avg > 0 else 0
                ),
                recurring_vs_discretionary_ratio=0.5, # Placeholder
                savings_rate_trend=[0.2, 0.18, 0.15], # Placeholder
                impulse_spend_count=impulse_count,
                top_spending_personality=top_personality
            )

    async def compute_financial_stress_score(self, user_id: int) -> StressScoreResult:
        profile = await self.compute_behaviour_profile(user_id)
        score = 0
        signals = []
        
        if profile.month_start_vs_end_spend.ratio > 1.5:
            score += 20
            signals.append("Month-end spend spike detected")
            
        if profile.impulse_spend_count > 5:
            score += 15
            signals.append("High frequency of impulse purchases")
            
        # Simplified for demo
        if score < 20: level = "low"
        elif score < 50: level = "moderate"
        elif score < 75: level = "high"
        else: level = "critical"
        
        return StressScoreResult(
            score=min(score, 100),
            level=level,
            top_signals=signals,
            trend="stable"
        )

    async def detect_anomalies(self, user_id: int) -> List[AnomalyAlert]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Transaction).where(Transaction.user_id == user_id, Transaction.type == 'debit')
            )
            txns = result.scalars().all()
            
            if len(txns) < 30:
                return []
            
            # Prepare data for IsolationForest
            X = np.array([[t.amount, t.timestamp.hour, t.timestamp.weekday()] for t in txns])
            clf = IsolationForest(contamination=0.05, random_state=42)
            preds = clf.fit_predict(X)
            scores = clf.decision_function(X)
            
            anomalies = []
            for i, pred in enumerate(preds):
                if pred == -1: # Anomaly
                    t = txns[i]
                    anomalies.append(AnomalyAlert(
                        txn_id=t.txn_id,
                        amount=t.amount,
                        merchant=t.merchant_normalized or t.merchant_raw,
                        reason="Unusual amount or timing for your patterns",
                        anomaly_score=float(scores[i])
                    ))
            
            return sorted(anomalies, key=lambda x: x.anomaly_score)[:5]

    async def get_behaviour_insights(self, user_id: int) -> List[BehaviourInsight]:
        profile = await self.compute_behaviour_profile(user_id)
        insights = []
        
        if profile.weekend_vs_weekday_spend > 1.5:
            insights.append(BehaviourInsight(
                title="Weekend Spender",
                observation=f"You spend {profile.weekend_vs_weekday_spend:.1f}x more on weekends than weekdays.",
                impact="Concentrated spending makes budget tracking harder."
            ))
            
        if profile.month_start_vs_end_spend.ratio > 1.5:
            insights.append(BehaviourInsight(
                title="Month-End Pressure",
                observation="Your spending spikes significantly in the last week of the month.",
                impact="Increases risk of cash crunches before next salary."
            ))
            
        return insights
