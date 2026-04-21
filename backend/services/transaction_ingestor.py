# backend/services/transaction_ingestor.py
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import select
from backend.database import AsyncSessionLocal
from backend.models.transaction import Transaction, TransactionCategory
from backend.utils.merchant_normalizer import normalize
from backend.fraud.hooks import run_full_fraud_check

logger = logging.getLogger(__name__)

class IngestResult(BaseModel):
    processed: int
    duplicates_removed: int
    errors: List[str]
    transactions: List[int] # List of IDs

def deduplicate(transactions: List[dict]) -> List[dict]:
    # Group by amount and approximate timestamp
    deduped = []
    seen = {} # key: (amount, bucketed_timestamp)
    
    removed_count = 0
    for txn in transactions:
        amount = txn['amount']
        ts = datetime.fromisoformat(txn['timestamp'])
        # Bucket timestamp to 5 minutes
        ts_bucket = ts.replace(minute=(ts.minute // 5) * 5, second=0, microsecond=0)
        key = (amount, ts_bucket)
        
        if key in seen:
            prev_txn = seen[key]
            # If different source, it's likely a duplicate
            if txn['source'] != prev_txn['source']:
                removed_count += 1
                # Keep UPI if available
                if txn['source'] == 'UPI':
                    txn['source_also_seen_in'] = [prev_txn['source']]
                    seen[key] = txn
                else:
                    prev_txn.setdefault('source_also_seen_in', []).append(txn['source'])
                continue
        
        seen[key] = txn
    
    logger.info(f"Deduplication removed {removed_count} transactions")
    return list(seen.values())

class TransactionIngestor:
    
    async def ingest(self, raw_transactions: List[dict], user_id: int, source: str) -> IngestResult:
        deduped_raw = deduplicate(raw_transactions)
        
        processed_txns = []
        errors = []
        duplicates_removed = len(raw_transactions) - len(deduped_raw)
        
        async with AsyncSessionLocal() as session:
            # Load user history for tagging and recurring detection
            result = await session.execute(select(Transaction).where(Transaction.user_id == user_id))
            history = result.scalars().all()
            
            for raw in deduped_raw:
                try:
                    # FRAUD_HOOK
                    fraud_res = run_full_fraud_check(user_id, {"amount": raw['amount'], "merchant": raw['merchant_raw']})
                    if fraud_res.status == "block":
                        errors.append(f"Transaction blocked by fraud check: {raw['txn_id']}")
                        continue

                    txn = self._parse(raw, source, user_id)
                    if not txn:
                        errors.append(f"Parse failure for txn: {raw.get('txn_id')}")
                        continue
                    
                    txn = self._normalize_merchant(txn)
                    txn.is_recurring = self._detect_recurring(txn, history)
                    txn.spending_personality_tag = self._tag_personality(txn, history)
                    
                    session.add(txn)
                    processed_txns.append(txn)
                except Exception as e:
                    errors.append(f"Error processing txn {raw.get('txn_id')}: {str(e)}")
            
            await session.commit()
            for t in processed_txns:
                await session.refresh(t)
                
        return IngestResult(
            processed=len(processed_txns),
            duplicates_removed=duplicates_removed,
            errors=errors,
            transactions=[t.id for t in processed_txns]
        )

    def _parse(self, raw: dict, source: str, user_id: int) -> Optional[Transaction]:
        try:
            return Transaction(
                user_id=user_id,
                txn_id=raw.get('txn_id') or str(uuid.uuid4()),
                amount=raw['amount'],
                type=raw.get('type', 'debit'),
                merchant_raw=raw['merchant_raw'],
                source=source,
                timestamp=datetime.fromisoformat(raw['timestamp']),
                balance_after=raw.get('balance_after'),
                description=raw.get('description')
            )
        except Exception:
            return None

    def _normalize_merchant(self, txn: Transaction) -> Transaction:
        res = normalize(txn.merchant_raw)
        txn.merchant_normalized = res.canonical_name
        txn.category = TransactionCategory(res.category)
        txn.sub_category = res.sub_category
        return txn

    def _tag_personality(self, txn: Transaction, history: List[Transaction]) -> Optional[str]:
        # Simple logic: If category spend > 30% of total in last 30 days
        relevant_history = [t for t in history if t.timestamp > datetime.now() - timedelta(days=30)]
        if len(relevant_history) < 10: return None # Need some history
        
        cat_spend = sum(t.amount for t in relevant_history if t.category == txn.category)
        total_spend = sum(t.amount for t in relevant_history if t.type == 'debit')
        
        if total_spend > 0 and (cat_spend / total_spend) > 0.3:
            tags = {
                TransactionCategory.FOOD: "Food Enthusiast",
                TransactionCategory.TRANSPORT: "Commuter",
                TransactionCategory.SHOPPING: "Shopaholic",
                TransactionCategory.UTILITIES: "Homebody",
                TransactionCategory.ENTERTAINMENT: "Entertainment Buff",
                TransactionCategory.HEALTH: "Health Conscious"
            }
            return tags.get(txn.category)
        return None

    def _detect_recurring(self, txn: Transaction, history: List[Transaction]) -> bool:
        # Same merchant, similar amount (±10%) in 2+ previous months
        matches = 0
        for h in history:
            if h.merchant_normalized == txn.merchant_normalized:
                if 0.9 * txn.amount <= h.amount <= 1.1 * txn.amount:
                    matches += 1
        return matches >= 2
