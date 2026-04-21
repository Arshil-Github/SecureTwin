# SecureWealth Twin — LLM Build Workflows

## What This Is

A set of sequenced prompt workflows to build the SecureWealth Twin app using an LLM (Claude or Gemini). Each file is a self-contained session you run with the LLM. Feed it the file, follow the steps, commit the output, then move to the next.

---

## Folder Structure

```
00_README.md               ← you are here — rules, conventions, token budget
01_project_scaffold.md     ← FastAPI skeleton, DB models, project structure
02_mock_data.md            ← realistic Indian financial mock data generation
03_transaction_ingestor.md ← clean, normalize, deduplicate raw transactions
04_spend_lens.md           ← categorization, merchant memory, personality tags
05_behaviour_engine.md     ← patterns, stress score, anomaly detection
06_wealth_mapper.md        ← investments, net worth snapshot, portfolio health
07_goal_engine.md          ← goals, health status, conflict detection
08_scenario_simulator.md   ← what-if projections, cost-of-inaction chart
09_strategy_engine.md      ← ranked wealth actions, ROI of behaviour change
10_insight_narrator.md     ← plain-language explanations, explainability layer
11_financial_calendar.md   ← upcoming SIPs, FD maturities, EMI alerts
12_ai_integration.md       ← Claude / Gemini provider toggle, prompt templates
13_api_routes.md           ← all FastAPI endpoints, request/response schemas
14_react_native_scaffold.md← Expo project, navigation, design tokens
15_rn_dashboard.md         ← net worth, goal cards, spending chart screens
16_rn_goals_and_sims.md    ← goal screen, scenario simulator UI
17_rn_portfolio.md         ← investment tracker, portfolio health screen
18_rn_ai_chat.md           ← conversational AI screen, nudges, explanations
19_security_stubs.md       ← fraud layer STUBS only — gaps for later integration
20_integration_test.md     ← end-to-end smoke test, demo data walkthrough
```

---

## Global Rules — Read Before Every Session

These rules apply to **every workflow file**. Paste them at the top of every LLM session as a system prompt or as the first message.

```
GLOBAL RULES — SECUREWEALTH TWIN

1. TOKEN EFFICIENCY
   - Never explain code you've just written unless asked.
   - No "Here is the code:" preambles or "Hope this helps!" closers.
   - Skip obvious docstrings. Only write docstrings for public API functions.
   - When asked to generate a file, output the full file once. Do not show diffs
     unless asked.
   - If a task can be done in fewer lines without sacrificing readability, do it.

2. CODE STYLE
   - Python: follow PEP8, use type hints everywhere, Pydantic v2 models.
   - React Native: functional components only, TypeScript strict mode.
   - No default exports except for React Native screens.
   - Folder structure must match what is defined in 01_project_scaffold.md.
   - Every new file must start with a one-line comment: # path/from/root/to/file.py

3. STUBS & GAPS (FRAUD LAYER)
   - Any function that will later connect to the fraud/cybersecurity layer
     must be marked with: # FRAUD_HOOK: <description>
   - These functions must be implemented as pass-through stubs that return
     {"fraud_check": "STUB", "status": "pass"} so the app works end-to-end
     without the fraud layer.
   - Do NOT implement any fraud logic. Only leave clean integration points.

4. MOCK DATA ONLY
   - This is a hackathon prototype. Never write code that calls real bank APIs.
   - All external data is loaded from /backend/mock_data/ JSON files.
   - The mock data layer must be swappable (use a DATA_SOURCE env var).

5. AI PROVIDER TOGGLE
   - All LLM calls must go through backend/services/ai_provider.py.
   - The provider is set by env var: AI_PROVIDER=claude or AI_PROVIDER=gemini.
   - Never call the AI SDK directly from a route or engine. Always via the provider module.

6. DATABASE
   - Use SQLite for local dev (no Docker needed for hackathon).
   - All models must also have a Pydantic schema mirror in /backend/schemas/.
   - Use Alembic for migrations, but include a create_all fallback for demo day.

7. REACT NATIVE
   - Use Expo SDK 54+.
   - All API calls go through /frontend/src/api/client.ts.
   - Never hardcode the backend URL; read from app.config.ts EXPO_PUBLIC_API_URL.
   - Use Zustand for global state. React Query for server state.

8. WHEN STUCK
   - If a requirement is ambiguous, implement the simpler interpretation and
     add a comment: # TODO: clarify — assumed <your interpretation>
   - Never ask clarifying questions mid-output. Make the call and move on.
```

---

## Workflow Sequencing

Run workflows **in order**. Each session depends on the previous.

| Phase | Files | Goal |
|-------|-------|------|
| Foundation | 01–02 | Repo skeleton, models, mock data |
| Backend Core | 03–11 | All 8 backend engines |
| AI & API | 12–13 | Provider toggle, all REST routes |
| Frontend | 14–18 | React Native screens |
| Integration | 19–20 | Fraud stubs + smoke test |

**Time estimate per session:** 20–45 minutes of LLM interaction + review.

---

## How to Run a Workflow Session

1. Open a new LLM conversation.
2. Paste the **Global Rules** block above as your first message.
3. Paste the target workflow file (e.g. `03_transaction_ingestor.md`) as your second message.
4. Follow the `STEPS` section sequentially — each step is one LLM prompt.
5. Copy the output to your repo immediately. Don't let context pile up.
6. Run the `VERIFY` checklist at the end before closing the session.

---

## Token-Saving Conventions

- Use `@file:<path>` to reference a file you've already built — the LLM should treat it as known context, not re-generate it.
- Once a module is built and verified, **never re-paste it** in a later session. Reference it by path.
- If a session is getting long, start a new one and paste only the relevant previously-built files.
- Prefer asking for **function signatures + docstrings first**, then full implementations. This lets you catch design errors cheaply.
