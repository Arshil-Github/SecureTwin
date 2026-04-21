# Workflow 02 — Mock Data Generation

**Goal:** Generate realistic Indian financial mock data for 3 user personas. This data is used throughout all backend services and drives the demo.

**Estimated tokens:** Medium. LLM generates Python scripts that produce JSON — don't ask it to output the raw JSON directly (too many tokens). Ask for the generator script.

**Prerequisites:** Workflow 01 complete. Models defined.

---

## Context to Paste

Paste Global Rules + this file. Also paste:
```
@file: backend/models/transaction.py
@file: backend/models/investment.py
@file: backend/schemas/wealth_snapshot.py
```

---

## STEPS

### Step 1 — Persona Definitions (define these yourself, paste as context)

```
We have 3 user personas. Reference these throughout all mock data generation.

PERSONA A — Priya Sharma
  Age: 28, Salaried software engineer, Mumbai
  Monthly income: ₹85,000
  Risk appetite: Moderate
  Goals: Emergency fund (₹3L, 1 year), Home down payment (₹15L, 5 years)
  Spending style: High food delivery, subscriptions, occasional travel
  Investments: 2 SIPs (₹5,000/month each), 1 FD (₹50,000)
  Stress signal: Spending spikes in last week of month

PERSONA B — Ramesh Kulkarni
  Age: 45, Business owner, Pune
  Monthly income: ₹2,20,000 (irregular — varies ±30%)
  Risk appetite: Conservative
  Goals: Retirement corpus (₹2Cr, 15 years), Son's education (₹25L, 8 years)
  Spending style: High utilities, staff salaries, stable lifestyle
  Investments: 3 FDs, 1 RD, PPF, small mutual fund SIP
  Stress signal: Income irregularity causes month-end cash crunches

PERSONA C — Ananya Iyer
  Age: 23, First job, Bengaluru
  Monthly income: ₹42,000
  Risk appetite: Aggressive (willing to learn)
  Goals: Emergency fund (₹1L, 8 months), First investment portfolio
  Spending style: High entertainment, dining, impulsive online shopping
  Investments: None yet — this is her starting point
  Stress signal: No savings buffer, lives paycheck to paycheck
```

### Step 2 — Transaction Generator Script

Prompt:
```
Write backend/mock_data/generate_mock_data.py

This script uses the Faker library to generate realistic mock data for the 
3 personas defined above. Run it once to produce JSON files in backend/mock_data/.

Generate for each persona:
- 6 months of transactions (180 days)
- Realistic Indian merchant names and UPI VPAs
- Mix of: Swiggy, Zomato, BigBasket, Amazon, Flipkart, Ola, Uber, 
  BESCOM/MSEB (electricity), Airtel/Jio, Netflix, Spotify, gym,
  salary credit, rent debit, EMI debit
- Include INTENTIONALLY DIRTY merchant strings for 20% of transactions:
  "SWGY*8823", "swiggy@icici", "SWG FOOD", "ZOMTO ORDER" 
  → so the Transaction Ingestor has real work to do
- Include some transactions that appear in BOTH UPI and bank statement
  (same amount, ±2 minute timestamp, slightly different description)
  → deduplication test cases
- Spending must match persona patterns (Priya: high food, Ananya: high entertainment)
- Include month-end spend spike for Priya and Ananya

Output files:
  backend/mock_data/transactions_priya.json
  backend/mock_data/transactions_ramesh.json
  backend/mock_data/transactions_ananya.json

Each JSON file: array of raw transaction objects using the Transaction model schema.
Include a metadata block at the top: persona_id, date_range, total_transactions.
```

### Step 3 — Investment & Asset Data

Prompt:
```
Extend generate_mock_data.py to also produce:

backend/mock_data/investments_priya.json
  - 2 mutual fund SIPs with 8 months of history
  - 1 FD (₹50,000, 7.1%, 1 year)
  - Use realistic scheme names: Axis Bluechip Fund, Mirae Asset Large Cap
  - NAV history showing realistic growth (not perfectly linear)
  - XIRR around 12-14% for equity funds

backend/mock_data/investments_ramesh.json
  - 3 FDs (laddered maturities: 3, 6, 12 months)
  - 1 RD (₹5,000/month, 18 months in)
  - PPF (15 years, 12 years complete, balance ₹18L)
  - 1 SIP (Mirae Asset Hybrid, ₹3,000/month, conservative)

backend/mock_data/investments_ananya.json
  - Empty array — she has no investments
  - Include a "recommended_first_steps" field in metadata with 3 starter actions

backend/mock_data/assets_priya.json
  - 2 assets: gold (10g, bought 2022), vehicle (Honda Activa)

backend/mock_data/assets_ramesh.json
  - 3 assets: commercial property (Pune), gold (50g), vehicle (Innova)

backend/mock_data/users.json
  - All 3 user records matching User model schema
  - Include hashed passwords (use bcrypt, password: "Demo@1234" for all)
  - trusted_devices: each user has 1 pre-registered device fingerprint

Also generate:
backend/mock_data/loader.py
  - Functions: load_user(persona_id), load_transactions(persona_id),
    load_investments(persona_id), load_assets(persona_id)
  - Checks DATA_SOURCE env var: if "mock", loads from JSON files
  - If "live", raises NotImplementedError with message "Live data source not implemented"
  - Used by all service layers to fetch data
```

### Step 4 — Seed Script

Prompt:
```
Write backend/mock_data/seed_db.py

This script:
1. Calls init_db() to create all tables
2. Loads all mock data JSON files via loader.py
3. Inserts all 3 users, their transactions, investments, assets into the database
4. Prints a summary: "Seeded X transactions, Y investments, Z assets for 3 users"
5. Is idempotent — running it twice does not duplicate data (use upsert on unique IDs)

Also add a make target or npm script so the team can run:
  make seed    → python -m backend.mock_data.seed_db
  make dev     → uvicorn backend.main:app --reload
```

---

## VERIFY Checklist

- [ ] `python backend/mock_data/generate_mock_data.py` — all JSON files created
- [ ] Priya's transactions contain dirty merchant strings (SWGY*, swiggy@icici)
- [ ] At least 5 duplicate transactions exist across UPI + bank sources
- [ ] `python backend/mock_data/seed_db.py` — runs without error
- [ ] Re-running seed_db.py — no duplicates added
- [ ] Ananya's investments JSON is empty array with metadata
- [ ] All 3 users loadable via loader.load_user(persona_id)

---

## Output to Commit

```
backend/mock_data/
  generate_mock_data.py
  seed_db.py
  loader.py
  transactions_priya.json
  transactions_ramesh.json
  transactions_ananya.json
  investments_priya.json
  investments_ramesh.json
  investments_ananya.json
  assets_priya.json
  assets_ramesh.json
  users.json
Makefile (or package.json scripts)
```
