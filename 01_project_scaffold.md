# Workflow 01 — Project Scaffold

**Goal:** Generate the full repo skeleton, all folder structures, base config files, DB setup, and empty module stubs. Nothing runs yet — this is the skeleton everything else hangs off.

**Estimated tokens:** Low. Mostly structure, no logic yet.

**Prerequisites:** None. This is the first session.

---

## Context to Paste

Paste the Global Rules from `00_README.md` first, then paste this file.

---

## STEPS

### Step 1 — Repo & Folder Structure

Prompt:
```
Create the following folder structure for the SecureWealth Twin project.
Output a shell script (setup.sh) that creates every folder and empty __init__.py 
/ index.ts file. Do not output the individual files yet — just the script.

Backend structure (FastAPI, Python 3.11):
backend/
  main.py                        # FastAPI app entry point
  config.py                      # env vars, settings
  database.py                    # SQLAlchemy engine + session
  models/
    user.py
    transaction.py
    investment.py
    goal.py
    asset.py
    audit_log.py
  schemas/
    user.py
    transaction.py
    investment.py
    goal.py
    asset.py
    wealth_snapshot.py
    action.py
  services/
    ai_provider.py               # Claude / Gemini toggle
    transaction_ingestor.py
    spend_lens.py
    behaviour_engine.py
    wealth_mapper.py
    goal_engine.py
    scenario_simulator.py
    strategy_engine.py
    insight_narrator.py
    financial_calendar.py
  routers/
    auth.py
    transactions.py
    investments.py
    goals.py
    wealth.py
    insights.py
    ai_chat.py
    calendar.py
  fraud/
    hooks.py                     # STUB file — all fraud integration points
  mock_data/
    users.json
    transactions.json
    investments.json
    assets.json
  utils/
    merchant_normalizer.py
    xirr.py
    date_helpers.py
  tests/
    conftest.py
    test_ingestor.py
    test_spend_lens.py
    test_goal_engine.py

Frontend structure (React Native, Expo SDK 54+, TypeScript):
frontend/
  app.config.ts
  App.tsx
  src/
    api/
      client.ts                  # Axios instance, base URL from env
      endpoints.ts               # all API endpoint strings
    store/
      useAuthStore.ts            # Zustand
      useWealthStore.ts
      useGoalStore.ts
    screens/
      Onboarding/
        WelcomeScreen.tsx
        KYCScreen.tsx
        RiskQuizScreen.tsx
        GoalSetupScreen.tsx
      Dashboard/
        DashboardScreen.tsx
        NetWorthCard.tsx
        SpendingChart.tsx
        GoalProgressCard.tsx
      Goals/
        GoalsScreen.tsx
        GoalDetailScreen.tsx
        ScenarioSimScreen.tsx
      Portfolio/
        PortfolioScreen.tsx
        PortfolioHealthCard.tsx
      Chat/
        AIChatScreen.tsx
      Settings/
        SettingsScreen.tsx
    navigation/
      RootNavigator.tsx
      AppNavigator.tsx
      OnboardingNavigator.tsx
    components/
      WealthCard.tsx
      ActionCard.tsx
      RiskBadge.tsx
      SkeletonLoader.tsx
      FraudWarningModal.tsx      # STUB — renders nothing for now
    theme/
      colors.ts
      typography.ts
      spacing.ts
    types/
      api.ts
      navigation.ts
```

### Step 2 — Config & Environment

Prompt:
```
Generate these files:

1. backend/config.py
   - Uses pydantic-settings BaseSettings
   - Fields: DATABASE_URL (default: sqlite:///./securewealth.db), 
     AI_PROVIDER (default: "claude"), ANTHROPIC_API_KEY, GEMINI_API_KEY,
     SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES (default: 60),
     DATA_SOURCE (default: "mock", options: "mock" | "live"),
     CORS_ORIGINS (list, default: ["*"])
   - Load from .env file
   - Export a singleton: settings = Settings()

2. backend/.env.example
   - All fields from Settings with placeholder values
   - Comment each field explaining what it does

3. frontend/app.config.ts
   - Expo config
   - EXPO_PUBLIC_API_URL env var, default http://localhost:8000
   - App name: SecureWealth Twin, slug: securewealth-twin
   - Android and iOS basic config
```

### Step 3 — Database Setup

Prompt:
```
Generate backend/database.py:
- SQLAlchemy async engine using DATABASE_URL from settings
- SessionLocal factory
- Base declarative class
- get_db() dependency for FastAPI
- init_db() function that calls Base.metadata.create_all (fallback for demo day)
- Also create alembic.ini and alembic/env.py configured for this project

The database must work with both SQLite (dev) and PostgreSQL (prod) 
without code changes — just the DATABASE_URL env var.
```

### Step 4 — All SQLAlchemy Models

Prompt:
```
Generate all SQLAlchemy models. Each file starts with # backend/models/<name>.py

backend/models/user.py:
  User: id, email, hashed_password, full_name, pan_number (encrypted),
  age, monthly_income, risk_appetite (enum: conservative/moderate/aggressive),
  is_kyc_verified, created_at, trusted_devices (JSON array of device fingerprints)

backend/models/transaction.py:
  Transaction: id, user_id (FK), txn_id (unique, source ID), amount, type
  (debit/credit), merchant_raw (original string), merchant_normalized,
  category (enum — see below), sub_category, source (UPI/bank/manual),
  timestamp, balance_after, description, is_recurring, spending_personality_tag

  Category enum: FOOD, TRANSPORT, SHOPPING, UTILITIES, ENTERTAINMENT,
  HEALTH, EDUCATION, EMI, INVESTMENT, INCOME, TRANSFER, OTHER

backend/models/investment.py:
  Investment: id, user_id (FK), account_type (mutual_fund/fd/rd/savings/stocks),
  folio_number, scheme_name, units_held, nav, current_value, invested_amount,
  sip_amount, sip_frequency, sip_date, start_date, last_transaction_date,
  returns_absolute, returns_xirr, maturity_date, interest_rate, principal,
  auto_renewal

backend/models/goal.py:
  Goal: id, user_id (FK), name, goal_type (time_bound/amount_bound/habit_bound),
  target_amount, target_date, current_amount, monthly_contribution,
  health_status (on_track/at_risk/off_track), priority (1-5), created_at

backend/models/asset.py:
  Asset: id, user_id (FK), asset_type (property/gold/vehicle/other),
  name, purchase_value, current_value, purchase_date, notes

backend/models/audit_log.py:
  AuditLog: id, user_id (FK), action_type, entity_type, entity_id,
  payload (JSON), fraud_check_result (JSON), timestamp
  # This table is used by both normal audit and the fraud layer hooks
```

### Step 5 — Pydantic Schemas

Prompt:
```
Generate Pydantic v2 schemas for all models. Mirror the SQLAlchemy models 
but split into Create / Read / Update variants where needed.

Also generate these composite schemas:

backend/schemas/wealth_snapshot.py:
  WealthSnapshot:
    user_id, snapshot_date,
    total_cash, total_investments, total_assets, total_liabilities,
    net_worth, net_worth_delta_mom (month-on-month change),
    portfolio_health_score (0-100),
    financial_stress_score (0-100),
    investments: list[InvestmentRead],
    assets: list[AssetRead]

backend/schemas/action.py:
  WealthAction:
    action_id, title, description, action_type
    (move_funds/rebalance/reduce_spend/increase_sip/tax_save/alert),
    impact_level (high/medium/low), urgency (immediate/this_week/this_month),
    expected_impact_description, goal_impact_score (optional float),
    data_payload (JSON — for frontend to deep-link to relevant screen)
```

### Step 6 — FastAPI App Entry Point

Prompt:
```
Generate backend/main.py:
- FastAPI app with title "SecureWealth Twin API", version "1.0.0"
- Include all routers from backend/routers/ (use placeholder includes for now 
  — the routers are empty stubs)
- CORS middleware using settings.CORS_ORIGINS
- Startup event: call init_db()
- Health check endpoint: GET /health → {"status": "ok", "ai_provider": settings.AI_PROVIDER}
- Global exception handler for ValueError → 400, for all others → 500
  with {"detail": str(e)} response

Generate backend/fraud/hooks.py:
- This file contains STUB functions for every fraud integration point
- Every function must:
  1. Accept the relevant context params
  2. Log to audit_log table
  3. Return {"fraud_check": "STUB", "status": "pass", "risk_score": 0, "risk_level": "low"}
  4. Be marked with # FRAUD_HOOK: <description>

Stub functions needed:
  - check_device_trust(user_id, device_fingerprint) → FraudCheckResult
  - check_session_speed(user_id, action_timestamp, login_timestamp) → FraudCheckResult
  - check_amount_anomaly(user_id, amount, category) → FraudCheckResult
  - check_otp_pattern(user_id, otp_attempt_count) → FraudCheckResult
  - check_first_time_action(user_id, action_type, entity_id) → FraudCheckResult
  - check_behaviour_consistency(user_id, action_sequence) → FraudCheckResult
  - run_full_fraud_check(user_id, action_context: dict) → FraudCheckResult
    # This is the main entry point — calls all checks and aggregates

FraudCheckResult Pydantic model:
  fraud_check: Literal["STUB", "ACTIVE"]
  status: Literal["pass", "warn", "block"]
  risk_score: int (0-100)
  risk_level: Literal["low", "medium", "high"]
  triggered_signals: list[str]
  message: str
```

### Step 7 — Dependency & Run Files

Prompt:
```
Generate:

1. backend/requirements.txt
   Include: fastapi, uvicorn[standard], sqlalchemy, alembic, pydantic, 
   pydantic-settings, python-jose[cryptography], passlib[bcrypt], 
   python-multipart, anthropic, google-generativeai, scikit-learn, 
   pandas, numpy, statsmodels, prophet, shap, redis, celery, 
   python-dotenv, httpx, faker

2. frontend/package.json
   Include expo ~54.0.0, react-native, typescript, @react-navigation/native,
   @react-navigation/stack, @react-navigation/bottom-tabs,
   expo-secure-store, expo-local-authentication,
   react-native-mmkv, zustand, @tanstack/react-query,
   axios, react-native-paper, nativewind, 
   victory-native (for charts), react-native-svg,
   @expo/vector-icons

3. frontend/src/api/client.ts
   - Axios instance
   - baseURL from process.env.EXPO_PUBLIC_API_URL
   - Request interceptor: attach JWT from SecureStore
   - Response interceptor: on 401, clear auth and redirect to login
   - Export typed get/post/put/delete helpers

4. frontend/src/theme/colors.ts, typography.ts, spacing.ts
   Color palette for a premium fintech app:
   - Deep navy primary (#0A1628)
   - Electric teal accent (#00D4AA)  
   - Warm gold highlight (#F5A623)
   - Soft white surface (#F8FAFB)
   - Danger red (#E53E3E), Warning amber (#F6AD55)
   - Full semantic token set (background, surface, border, text variants)
   Typography: use DM Sans for body, Playfair Display for large numbers/headings
   Spacing: 4px base grid, scale 1-12
```

---

## VERIFY Checklist

Before closing this session, confirm:

- [ ] `setup.sh` runs without errors — all folders created
- [ ] `backend/config.py` loads from `.env` without crashing
- [ ] `backend/database.py` — `init_db()` runs, SQLite file created
- [ ] All 6 SQLAlchemy models import without error
- [ ] `python -c "from backend.main import app"` works
- [ ] `fraud/hooks.py` — every stub returns `FraudCheckResult` with `fraud_check: "STUB"`
- [ ] `frontend/src/api/client.ts` — TypeScript compiles
- [ ] Theme files export all expected tokens

---

## Output to Commit

```
backend/
  main.py, config.py, database.py, requirements.txt
  models/ (all 6 files)
  schemas/ (all files)
  fraud/hooks.py
  .env.example
frontend/
  package.json, app.config.ts
  src/api/client.ts
  src/theme/ (all 3 files)
setup.sh
```
