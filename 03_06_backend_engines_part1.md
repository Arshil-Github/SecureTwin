# Workflow 03 — Transaction Ingestor

**Goal:** Build the data cleaning layer that normalizes raw transaction input before any analysis happens.

**Estimated tokens:** Medium. Core logic is fuzzy matching and deduplication.

**Prerequisites:** Workflows 01–02 complete.

---

## Context to Paste

```
@file: backend/models/transaction.py
@file: backend/schemas/transaction.py
@file: backend/mock_data/loader.py
```

---

## STEPS

### Step 1 — Merchant Normalizer

Prompt:
```
Write backend/utils/merchant_normalizer.py

This module normalizes dirty merchant name strings to canonical names.

Requirements:
- Maintain a MERCHANT_MAP dict: maps regex patterns → canonical name + category
- Include at minimum: Swiggy, Zomato, BigBasket, Amazon, Flipkart, Ola, Uber,
  Netflix, Spotify, Airtel, Jio, BESCOM, MSEB, salary patterns, rent patterns
- Pattern matching order: exact match → regex match → fuzzy match (difflib)
- fuzzy threshold: 80% similarity
- normalize(raw_string: str) → MerchantResult(canonical_name, category, sub_category, confidence)
- cache results in a module-level dict (avoid re-computing same string)
- Unknown merchants → category=OTHER, canonical_name=raw_string.title()

Write a small test at the bottom under if __name__ == "__main__":
that tests: "SWGY*8823", "swiggy@icici", "SWG FOOD", "ZOMTO ORDER",
"NFLX.COM", "BESCOM BILL", "SAL CREDIT INFOSYS"
```

### Step 2 — Deduplication Logic

Prompt:
```
Write the deduplication function in backend/services/transaction_ingestor.py

def deduplicate(transactions: list[dict]) -> list[dict]:
  Two transactions are duplicates if:
  - Same user_id
  - Same amount (exact)
  - Timestamps within 5 minutes of each other
  - Different source (UPI vs bank) — same-source duplicates are errors, keep both
  
  Return the deduplicated list. For each duplicate pair, keep the UPI version 
  (more metadata), attach source_also_seen_in: ["bank"] to the kept record.
  Log how many duplicates were removed.
```

### Step 3 — Full Ingestor Service

Prompt:
```
Complete backend/services/transaction_ingestor.py

class TransactionIngestor:
  
  def ingest(self, raw_transactions: list[dict], user_id: int, 
             source: str) -> IngestResult:
    """
    Full pipeline: parse → normalize → deduplicate → tag → persist
    Returns IngestResult(processed: int, duplicates_removed: int, 
                         errors: list[str], transactions: list[Transaction])
    """
  
  def _parse(self, raw: dict, source: str) -> Transaction | None:
    """Parse one raw dict → Transaction model. Return None on parse failure."""
  
  def _normalize_merchant(self, txn: Transaction) -> Transaction:
    """Apply merchant_normalizer, set merchant_normalized + category + sub_category"""
  
  def _tag_personality(self, txn: Transaction, 
                       user_history: list[Transaction]) -> Transaction:
    """
    Assign spending_personality_tag based on category spend over user history.
    Tags: "Food Enthusiast", "Commuter", "Shopaholic", "Homebody", 
          "Entertainment Buff", "Health Conscious", "Saver"
    Only tag if user has 30+ days of history in that category.
    """
  
  def _detect_recurring(self, txn: Transaction,
                        user_history: list[Transaction]) -> bool:
    """
    Mark transaction as recurring if same merchant + similar amount 
    appears in 2+ previous months.
    """

Also write the router endpoint:
POST /transactions/ingest
  Body: list of raw transaction dicts + source field
  Calls run_full_fraud_check() stub before persisting # FRAUD_HOOK
  Returns IngestResult
```

---

## VERIFY Checklist

- [ ] `normalize("SWGY*8823")` → canonical: "Swiggy", category: FOOD
- [ ] `normalize("BESCOM BILL")` → category: UTILITIES
- [ ] Deduplication removes the 5 known duplicates in Priya's mock data
- [ ] `ingest()` on Priya's raw transactions — 0 errors, correct counts
- [ ] Personality tags assigned after 30+ days (not before)
- [ ] FRAUD_HOOK comment present on ingest route

---

# Workflow 04 — Spend Lens

**Goal:** Build the categorization, merchant memory, and spending personality analysis layer.

**Prerequisites:** Workflow 03 complete (Transaction Ingestor working).

---

## Context to Paste

```
@file: backend/services/transaction_ingestor.py
@file: backend/models/transaction.py
@file: backend/utils/merchant_normalizer.py
```

---

## STEPS

### Step 1 — Spend Summary Engine

Prompt:
```
Write backend/services/spend_lens.py

class SpendLens:

  def get_spend_summary(self, user_id: int, period_days: int = 30) -> SpendSummary:
    """
    Returns:
      SpendSummary:
        period: (start_date, end_date)
        total_spend: float
        total_income: float
        savings_rate: float  # (income - spend) / income
        by_category: dict[Category, CategorySummary]
        top_merchants: list[MerchantSpend]  # top 5 by amount
        overspend_alerts: list[OverspendAlert]
        mom_comparison: dict[Category, float]  # % change vs last period
    """

  def get_category_summary(self, user_id: int, category: str, 
                            period_days: int = 30) -> CategorySummary:
    """
    CategorySummary:
      category, total_spend, transaction_count, avg_transaction,
      sub_categories: dict[str, float],
      personality_tag: str | None,
      top_merchants: list[MerchantSpend]
    """

  def detect_overspend(self, user_id: int) -> list[OverspendAlert]:
    """
    Compare last 30 days vs 3-month average per category.
    Raise alert if current period > 120% of average.
    OverspendAlert: category, current_spend, average_spend, 
                    pct_over, human_message
    human_message example: 
      "You spent ₹6,400 on Food this month — 34% above your usual ₹4,780"
    """

  def get_merchant_memory(self, user_id: int) -> dict[str, MerchantMemory]:
    """
    Returns all merchants this user has transacted with + their learned category.
    Users can override — store overrides in a user_merchant_overrides table.
    """

  def apply_user_recategorization(self, user_id: int, txn_id: int, 
                                   new_category: str) -> None:
    """
    Let user correct a category. Store the merchant → category mapping 
    so future transactions from that merchant are auto-corrected.
    # This creates a feedback loop — important for demo explainability
    """
```

### Step 2 — Spend Lens Router

Prompt:
```
Write backend/routers/transactions.py

Endpoints:
  GET  /transactions/summary?period_days=30       → SpendSummary
  GET  /transactions/category/{category}?period=30 → CategorySummary  
  GET  /transactions/overspend                    → list[OverspendAlert]
  GET  /transactions/merchants                    → dict merchant memory
  PUT  /transactions/{txn_id}/category            → recategorize, returns updated txn
  GET  /transactions/list?limit=50&offset=0       → paginated transaction list

All endpoints require auth (JWT dependency).
All write endpoints call run_full_fraud_check() stub. # FRAUD_HOOK
```

---

## VERIFY Checklist

- [ ] Priya's spend summary shows FOOD as top category
- [ ] Overspend alert fires for Ananya's entertainment category
- [ ] Recategorization persists across requests
- [ ] mom_comparison calculates correctly (needs 2 periods of data)
- [ ] FRAUD_HOOK on PUT /transactions/{txn_id}/category

---

# Workflow 05 — Behaviour Engine

**Goal:** Build the pattern analysis layer — spending patterns, financial stress score, and anomaly detection.

**Prerequisites:** Workflows 03–04 complete.

---

## Context to Paste

```
@file: backend/services/spend_lens.py
@file: backend/models/transaction.py
```

---

## STEPS

### Step 1 — Behavioural Feature Extraction

Prompt:
```
Write backend/services/behaviour_engine.py

class BehaviourEngine:

  def compute_behaviour_profile(self, user_id: int) -> BehaviourProfile:
    """
    BehaviourProfile:
      spend_to_income_ratio: dict[Category, float]  # % of income per category
      weekend_vs_weekday_spend: float  # ratio: weekend_avg / weekday_avg
      month_start_vs_end_spend: MonthSpendPattern
        # month_start_7d_avg vs month_end_7d_avg — stress indicator
      recurring_vs_discretionary_ratio: float
      savings_rate_trend: list[float]  # last 6 months, should be going up
      impulse_spend_count: int  # transactions > 2x category avg, last 30d
      top_spending_personality: str  # from personality tags
    """

  def compute_financial_stress_score(self, user_id: int) -> StressScoreResult:
    """
    Score 0-100. Higher = more stress. Derived ONLY from behaviour, not wealth.
    
    Signals (weights):
      - Savings rate declining 3 months in a row: +25
      - EMI-to-income ratio > 40%: +20
      - Month-end spend spike (last 7d of month > 1.5x month avg): +20
      - Impulse transactions > 5 in last 30d: +15
      - Zero investment transactions in last 90d: +10
      - Income irregular (std dev > 20% of mean): +10
    
    Returns:
      StressScoreResult:
        score: int
        level: "low" | "moderate" | "high" | "critical"
        top_signals: list[str]  # human-readable list of what's contributing
        trend: "improving" | "stable" | "worsening"  # vs last month
    """

  def detect_anomalies(self, user_id: int) -> list[AnomalyAlert]:
    """
    Unsupervised anomaly detection using IsolationForest from scikit-learn.
    Features per transaction: amount, hour_of_day, day_of_week, category_encoded
    
    Flag top 5 most anomalous transactions in last 30 days.
    AnomalyAlert: txn_id, amount, merchant, reason (human-readable), anomaly_score
    
    Note: IsolationForest needs at least 30 transactions to be meaningful.
    Under 30 → return [] with a note in metadata.
    """

  def get_behaviour_insights(self, user_id: int) -> list[BehaviourInsight]:
    """
    Synthesize profile + stress score → 3-5 plain observations.
    These are NOT recommendations — just observations.
    Example: "You spend 60% more on weekends than weekdays"
    Example: "Your savings rate has dropped from 22% to 14% over 3 months"
    These will be passed to the Insight Narrator for final language polish.
    """
```

### Step 2 — Behaviour Router

Prompt:
```
Add to backend/routers/transactions.py (or create behaviour.py):

  GET /behaviour/profile           → BehaviourProfile
  GET /behaviour/stress-score      → StressScoreResult
  GET /behaviour/anomalies         → list[AnomalyAlert]
  GET /behaviour/insights          → list[BehaviourInsight]
```

---

## VERIFY Checklist

- [ ] Ananya's stress score is HIGH (no savings, impulse spend, no investments)
- [ ] Priya's month-end spike is detected in month_start_vs_end_spend
- [ ] IsolationForest returns [] for Ananya if she has < 30 transactions
- [ ] Stress score trend shows "worsening" for Ananya
- [ ] Behaviour insights are plain English, no jargon

---

# Workflow 06 — Wealth Mapper

**Goal:** Build the investment data layer — net worth computation, portfolio health scoring, and the Wealth Snapshot.

**Prerequisites:** Workflow 01 (models), Workflow 02 (mock investment data).

---

## Context to Paste

```
@file: backend/models/investment.py
@file: backend/models/asset.py
@file: backend/schemas/wealth_snapshot.py
@file: backend/mock_data/loader.py
```

---

## STEPS

### Step 1 — XIRR Utility

Prompt:
```
Write backend/utils/xirr.py

Implement XIRR (Extended Internal Rate of Return) approximation:
  xirr(cashflows: list[tuple[date, float]]) → float

- cashflows: list of (date, amount) pairs. Investments are negative, 
  redemptions/current_value are positive.
- Use scipy.optimize.brentq or a Newton-Raphson implementation.
- Return annualized rate as a float (0.12 = 12%).
- Handle edge cases: single cashflow, all same date, non-convergence (return None).
- Write 3 test cases at the bottom: simple SIP that should give ~12%, 
  FD that should give ~7%, and edge case with single cashflow.
```

### Step 2 — Wealth Mapper Service

Prompt:
```
Write backend/services/wealth_mapper.py

class WealthMapper:

  def get_wealth_snapshot(self, user_id: int) -> WealthSnapshot:
    """
    Build the unified wealth picture:
    - total_cash: sum of savings account balances
    - total_investments: sum of current_value across all investments
    - total_assets: sum of current_value across all assets
    - net_worth: cash + investments + assets (no liabilities for v1)
    - net_worth_delta_mom: compare vs last month's snapshot
    - portfolio_health_score: call _compute_portfolio_health()
    - financial_stress_score: call BehaviourEngine
    """

  def _compute_portfolio_health(self, user_id: int, 
                                 investments: list[Investment]) -> int:
    """
    Score 0-100. Higher = healthier.
    
    Factors (weighted):
      Diversification (30pts):
        - 3+ asset types: 30, 2 types: 20, 1 type: 10, 0: 0
      Return quality (30pts):
        - XIRR > 12%: 30, 8-12%: 20, 4-8%: 10, <4% or negative: 0
      Goal alignment (20pts):
        - Investments mapped to at least one goal: +20
      Emergency buffer (20pts):  
        - Cash > 3x monthly expense: 20, 1-3x: 10, <1x: 0
    
    Return score + breakdown dict for frontend display.
    """

  def flag_underperforming(self, investments: list[Investment]) -> list[str]:
    """
    Return human-readable flags:
    - FD rate < current repo rate (hardcode 6.5% for demo) → "Real loss after inflation"
    - Equity SIP with XIRR < 8% after 2+ years → "Underperforming benchmark"
    - Large cash sitting in savings (>6 months expenses) → "Cash drag on net worth"
    """

  def get_investment_summary(self, user_id: int) -> InvestmentSummary:
    """
    InvestmentSummary:
      total_invested, current_value, absolute_return_pct,
      xirr_overall, by_type: dict[str, TypeSummary],
      upcoming_maturities: list[MaturityAlert]  # FDs/RDs maturing in 30d
      underperforming_flags: list[str]
    """

Add to backend/routers/wealth.py:
  GET /wealth/snapshot          → WealthSnapshot
  GET /wealth/investments        → InvestmentSummary
  POST /wealth/assets            → Add manual asset (calls fraud stub) # FRAUD_HOOK
  PUT /wealth/assets/{id}        → Update asset value
  GET /wealth/portfolio-health   → {score: int, breakdown: dict}
```

---

## VERIFY Checklist

- [ ] Ramesh's portfolio health score is higher than Ananya's (she has nothing)
- [ ] XIRR on Priya's SIP returns ~12-14%
- [ ] Ananya's emergency buffer flags as 0/20 (no investments)
- [ ] FD with 7.1% rate does NOT flag as underperforming (above 6.5% repo)
- [ ] `get_wealth_snapshot()` returns all fields, no KeyErrors
