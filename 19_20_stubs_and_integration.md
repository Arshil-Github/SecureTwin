# Workflow 19 — Fraud Layer Stubs & Integration Points

**Goal:** Audit all FRAUD_HOOK points, ensure every stub is clean and well-documented, and create the integration map so the cybersecurity layer can be dropped in later with minimal friction.

**This workflow produces NO new features.** It is a hardening + documentation pass.

**Prerequisites:** All previous workflows complete. App runs end-to-end.

---

## Context to Paste

```
@file: backend/fraud/hooks.py
@file: backend/routers/auth.py
@file: backend/routers/transactions.py
@file: backend/routers/goals.py
@file: backend/routers/wealth.py
@file: frontend/src/components/FraudWarningModal.tsx
```

---

## STEPS

### Step 1 — Audit All FRAUD_HOOKs

Prompt:
```
Search all files in the project for the string "FRAUD_HOOK".
List every occurrence as a table:

FILE | LINE | FUNCTION | HOOK_TYPE | CURRENT_BEHAVIOR | INTEGRATION_NOTES

Then verify: every occurrence in a router calls run_full_fraud_check() 
from backend/fraud/hooks.py before any state-mutating operation.

If any router writes to the DB without calling a fraud hook, add the hook call.
Do not implement fraud logic — only ensure the stub is called.
```

### Step 2 — Fraud Integration Specification

Prompt:
```
Write backend/fraud/INTEGRATION_GUIDE.md

This document is for the cybersecurity team who will implement the actual fraud layer.

Include:

## Overview
What the stubs do now, what they need to do in the final implementation.

## FraudCheckResult Schema
Full Pydantic model with all fields and valid values.
Document what each field means and how the frontend uses it.

## Hook Inventory
For each hook function in hooks.py:
  - Function signature
  - Input parameters and their sources
  - Current stub behavior
  - Expected real behavior (what signals to check, what data to access)
  - Database tables it should read/write

## Frontend Integration Points
Document FraudWarningModal.tsx:
  - Current behavior (pass-through for "low", placeholder modal for medium/high)
  - Required behavior: 
    - low → silent pass
    - medium → show warning modal, user must confirm, add 5s cooling-off timer
    - high → block action, show reason, show "Call your bank" button
  - Props interface that must not change (so cybersecurity team doesn't break frontend)

## Redis Keys Used by Fraud Layer
Pre-define the Redis key patterns the fraud layer should use:
  - session:{user_id}:login_time
  - session:{user_id}:action_count
  - otp:{user_id}:attempts:{action_type}
  - device:{user_id}:fingerprints (set)
  - action_history:{user_id} (sorted set, score=timestamp)

## Testing the Fraud Layer
How to trigger each risk level in demo mode:
  - Low: normal actions with trusted device
  - Medium: 3 rapid actions in 10 seconds (simulate via demo endpoint)
  - High: amount > 5x historical average (use demo data)
  - Provide: curl commands for each scenario
```

### Step 3 — Frontend Fraud Stub Polish

Prompt:
```
Update frontend/src/components/FraudWarningModal.tsx

The stub must be clean enough that replacing it requires only internal changes:

Requirements:
1. Accept the full FraudCheckResult as a prop (even though most fields are ignored now)
2. For risk_level "low": call onConfirm() immediately (no UI shown)
3. For risk_level "medium": show a simple confirmation modal
   - Title: "Please confirm"
   - Body: result.message || "This action requires your confirmation."
   - Two buttons: Cancel, Confirm
   - Add a comment: // FRAUD_HOOK: Add 5-second cooling-off timer here
4. For risk_level "high": show a blocking modal
   - Title: "Action blocked"
   - Body: result.message || "This action has been blocked for your security."
   - One button: "OK, I understand"
   - Add a comment: // FRAUD_HOOK: Add "Call your bank" button here
5. Add prop: onFraudEvent?: (result: FraudCheckResult) => void
   // FRAUD_HOOK: Hook for audit logging, analytics — implement when fraud layer added

All STUB behavior must be clearly marked with comments.
The component interface must not need changes when the real fraud layer is added.
```

---

## VERIFY Checklist

- [ ] FRAUD_HOOK audit table covers every route file
- [ ] No state-mutating route is missing a fraud hook call
- [ ] `INTEGRATION_GUIDE.md` covers all 6 hook functions
- [ ] `FraudWarningModal` renders correctly for all 3 risk levels
- [ ] Redis key patterns are pre-defined (even though Redis isn't used yet)
- [ ] Every stub returns `fraud_check: "STUB"` — easy to grep and find all stubs

---

# Workflow 20 — Integration Test & Demo Walkthrough

**Goal:** Verify the full app works end-to-end for all 3 personas. Produce a demo script. Fix any broken connections.

**Prerequisites:** All previous workflows complete. Both backend and frontend running.

---

## Context to Paste

Paste only the Global Rules. No file context needed — this session is about testing, not building.

---

## STEPS

### Step 1 — Backend Smoke Test Script

Prompt:
```
Write backend/tests/test_integration.py

A pytest integration test that runs through the full user journey for Persona A (Priya).
Use httpx.AsyncClient against the running FastAPI app.

Test sequence:
  1. POST /auth/register (Priya's data) → assert 201, get token
  2. POST /transactions/ingest (load Priya's mock transactions) → assert IngestResult
  3. GET /transactions/summary → assert categories present, total_spend > 0
  4. GET /behaviour/stress-score → assert score is a number 0-100
  5. GET /wealth/snapshot → assert net_worth > 0, portfolio_health_score present
  6. POST /goals (create Home goal) → assert GoalStatus returned
  7. GET /goals/conflicts → assert runs without error
  8. POST /simulate/multi (3 scenarios) → assert chart_data.series has 4 items
  9. GET /insights/actions → assert 1-5 actions returned
  10. POST /chat/message ("How much should I save for retirement?") → assert response text
  11. GET /calendar/upcoming → assert events list returned
  12. GET /demo/reset/priya (with DEMO_MODE=true) → assert reset message

Each test: print timing. Total should be under 30 seconds.
Mark any slow tests (>3s) with @pytest.mark.slow
```

### Step 2 — Frontend Manual Test Checklist

Prompt:
```
Generate a markdown checklist for manual QA of the React Native app.
Cover all screens and the key flows judges will exercise.

Format: grouped by screen, each item is a checkbox.
Include: happy path, empty states, loading states, error states.

Priority mark: ⭐ = must work for demo, no star = nice to have.

Generate the checklist for:
  - Onboarding (new user → Ananya's profile)
  - Dashboard (Priya's data)
  - Goals screen + goal detail (Ramesh's data — 2 goals, conflict)
  - Scenario Simulator (interactive slider test)
  - Portfolio screen (Ramesh's investments + Ananya's empty state)
  - AI Chat (3 test questions listed below)
  - Demo reset flow (demo day: how to switch personas)

Test questions for AI Chat:
  Q1: "How much should I be saving each month for my home goal?"
  Q2: "Why is my stress score high?"  
  Q3: "What's the best thing I can do with ₹10,000 right now?"
```

### Step 3 — Demo Day Script

Prompt:
```
Write DEMO_SCRIPT.md — a 5-minute demo walkthrough for the hackathon judges.

Structure:
  ## Setup (before judges arrive)
  - Commands to start backend + frontend
  - Demo reset commands for each persona

  ## 5-Minute Demo Flow
  Minute 1: Onboarding + Risk Profile (use Ananya — shows empty state + first-time user)
  Minute 2: Dashboard (switch to Priya — shows full data, stress score, wealth actions)
  Minute 3: Scenario Simulator (show "cost of inaction" — most visually striking feature)
  Minute 4: AI Chat (ask Q2 from test questions above — stress score explanation)
  Minute 5: Portfolio Health + Fraud Stub (show Ramesh's portfolio, explain fraud hooks)
  
  ## Talking Points per Feature
  For each feature: one sentence what it does, one sentence what makes it different.
  Include the "unorthodox edges" from the backend architecture doc.
  
  ## If Something Breaks
  - Backend crash → show mock data fallback (screenshots)
  - AI API fails → explain the template fallback (it still works)
  - Frontend crash → use browser dev build as backup
  
  ## Questions Judges Typically Ask
  5 likely questions + suggested answers.
```

---

## VERIFY Checklist

- [ ] All 12 integration tests pass
- [ ] No test takes > 5 seconds
- [ ] Manual QA checklist: all ⭐ items pass for at least 1 persona
- [ ] Demo script timed: 5 minutes max with rehearsal
- [ ] `GET /health` returns correct AI provider
- [ ] `GET /demo/personas` returns all 3 personas

---

## Final Commit Checklist

Before submitting to hackathon, verify:

- [ ] `.env.example` committed, `.env` in `.gitignore`
- [ ] `DEMO_MODE=false` in production config
- [ ] No hardcoded API keys anywhere in code
- [ ] All `# FRAUD_HOOK:` comments present and descriptive
- [ ] `backend/fraud/INTEGRATION_GUIDE.md` complete
- [ ] `README.md` includes: setup instructions, demo personas, AI provider toggle
- [ ] All 3 personas loadable via `/demo/reset/{persona}`
- [ ] App name visible everywhere: "SecureWealth Twin"
