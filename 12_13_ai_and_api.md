# Workflow 12 — AI Provider Integration

**Goal:** Build the provider toggle module and all prompt templates. This is the single file all AI calls must go through.

**Estimated tokens:** Medium. Mostly prompt engineering, not complex logic.

**Prerequisites:** Workflow 01 (config + env setup).

---

## Context to Paste

```
@file: backend/config.py
@file: backend/services/insight_narrator.py  (for context on how AI is used)
```

---

## STEPS

### Step 1 — AI Provider Module

Prompt:
```
Write backend/services/ai_provider.py

This is the ONLY file in the project that imports anthropic or google.generativeai.
All other services call this module.

class AIProvider:
  
  def __init__(self):
    self.provider = settings.AI_PROVIDER  # "claude" or "gemini"
    self._claude_client = None
    self._gemini_model = None

  def _get_claude(self):
    """Lazy init Claude client."""
    if not self._claude_client:
      import anthropic
      self._claude_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return self._claude_client

  def _get_gemini(self):
    """Lazy init Gemini model."""
    if not self._gemini_model:
      import google.generativeai as genai
      genai.configure(api_key=settings.GEMINI_API_KEY)
      self._gemini_model = genai.GenerativeModel("gemini-2.0-flash")
    return self._gemini_model

  async def complete(self, prompt: str, system: str = "", 
                     max_tokens: int = 500,
                     temperature: float = 0.3) -> AIResponse:
    """
    AIResponse: text: str, provider: str, tokens_used: int, 
                latency_ms: int, error: str | None
    
    If provider call fails: return AIResponse with error, text=""
    Log every call: provider, tokens_used, latency — for token budget tracking.
    """

  async def complete_structured(self, prompt: str, system: str,
                                  output_schema: dict,
                                  max_tokens: int = 800) -> dict | None:
    """
    Return parsed JSON matching output_schema.
    
    For Claude: use tool_use / function calling to enforce schema.
    For Gemini: use response_schema parameter.
    
    Returns None on failure (caller must handle gracefully).
    max_tokens: 800 hard limit for structured calls.
    """

# Export singleton
ai_provider = AIProvider()
```

### Step 2 — Prompt Templates

Prompt:
```
Write backend/services/prompts.py

All system and user prompts for the app. Keep prompts SHORT — token efficiency 
is mandatory. Each prompt must have a comment showing its approximate token count.

SYSTEM_PROMPTS = {

  "wealth_advisor": """  # ~60 tokens
    You are a concise Indian personal finance assistant. 
    Give specific, actionable advice. Use ₹ for amounts.
    Never guarantee returns. Always say "for simulation purposes."
    Respond in 2-3 sentences max unless asked for more.
    """,

  "narrator": """  # ~40 tokens
    Rewrite the provided financial insight in a warm, encouraging tone.
    Keep all numbers exact. Maximum 3 sentences. No jargon.
    """,

  "goal_advisor": """  # ~50 tokens
    You help users set and achieve financial goals in India.
    Be specific with amounts and timelines. 
    When suggesting SIPs, reference real fund categories (not specific funds).
    """,
}

USER_PROMPT_TEMPLATES = {

  "chat_response": """  # ~30 tokens + context
    User: {user_message}
    Context: {context_json}
    Answer in 2-3 sentences. If calculation needed, show it briefly.
    """,

  "explain_recommendation": """  # ~20 tokens + action
    Explain this in simple terms: {action_description}
    One sentence why, one sentence what to do.
    """,

  "narrator_rewrite": """  # ~15 tokens + text
    Original: {template_output}
    Rewrite warmer. Keep all numbers. Max 3 sentences.
    """,

  "goal_setup": """  # ~25 tokens + goal
    User wants: {goal_description}
    Suggest: target amount, timeline, monthly saving needed.
    Format as JSON: {{amount, months, monthly_saving, rationale}}
    """,

  "weekly_nudge": """  # ~30 tokens + summary
    Financial week summary: {summary_data}
    Write one encouraging sentence highlighting {positive_metric}.
    Start with the user's name: {user_name}.
    """,
}

def build_prompt(template_key: str, **kwargs) -> str:
  """Fill a prompt template. Raise ValueError if key not found."""

def estimate_tokens(text: str) -> int:
  """Rough token estimate: len(text) / 4. Good enough for budget tracking."""
```

### Step 3 — Chat Router

Prompt:
```
Write backend/routers/ai_chat.py

This router handles conversational AI — the chatbot screen.

Conversation state is kept CLIENT-SIDE (passed in each request) to avoid 
server-side session storage. Each request includes full history.
Max history to send: last 6 messages (3 turns) to control tokens.

POST /chat/message
  Body: ChatRequest
    user_message: str
    conversation_history: list[{role, content}]  # last 6 messages only
    user_id: int
  
  Steps:
    1. Load user's WealthSnapshot + top 3 WealthActions (for context)
    2. Build context_json from snapshot (keep it small: 5 key fields only)
    3. Call ai_provider.complete() with system=SYSTEM_PROMPTS["wealth_advisor"]
    4. Call insight_narrator.narrate_action() if response references an action
    5. Return ChatResponse: 
         assistant_message: str, 
         referenced_actions: list[WealthAction] | None,
         tokens_used: int

GET /chat/suggested-questions
  Returns 5 context-aware suggested questions based on user's current state.
  Rule-based (no LLM): pick from a bank of 20 questions based on which 
  signals are active (stress high → suggest stress-related questions, etc.)
  # This saves tokens — don't use LLM for question suggestions

POST /chat/explain/{action_id}
  Calls ai_provider.complete() with explain_recommendation template.
  max_tokens=200. Returns {explanation: str, tokens_used: int}
```

---

## VERIFY Checklist

- [ ] Switching `AI_PROVIDER=gemini` in .env → all calls use Gemini, no code change
- [ ] `complete()` returns AIResponse with error field on API failure (no exception)
- [ ] Chat history truncated to last 6 messages before sending
- [ ] `/chat/suggested-questions` uses zero AI tokens (rule-based only)
- [ ] `estimate_tokens()` called before every AI call — log if > budget

---

# Workflow 13 — API Routes & Auth

**Goal:** Complete all remaining API routes, authentication, and make sure every endpoint is wired up.

**Prerequisites:** All backend service workflows (03–12) complete.

---

## Context to Paste

```
@file: backend/main.py
@file: backend/config.py
@file: backend/models/user.py
@file: backend/fraud/hooks.py
```

---

## STEPS

### Step 1 — Auth System

Prompt:
```
Write backend/routers/auth.py

Use JWT (python-jose) + bcrypt (passlib).

Endpoints:

POST /auth/register
  Body: UserCreate (email, password, full_name, age, monthly_income, 
                    risk_appetite, device_fingerprint)
  - Hash password with bcrypt
  - Register device as trusted
  - Call check_device_trust() stub # FRAUD_HOOK
  - Return: UserRead + access_token

POST /auth/login
  Body: {email, password, device_fingerprint}
  - Verify password
  - Call check_device_trust() stub # FRAUD_HOOK
  - If new device: flag in response as new_device: true
  - Return: UserRead + access_token + is_new_device: bool

POST /auth/logout
  Invalidate token (add to a Redis blocklist — or simple in-memory set for demo)

GET /auth/me
  Return current user (from JWT)

PUT /auth/me
  Update profile fields. Re-run goal health calculations after income change.

Middleware: get_current_user dependency that validates JWT and returns User.
All protected routes use: current_user: User = Depends(get_current_user)
```

### Step 2 — Route Audit

Prompt:
```
Audit all routers. Produce a route map table:

METHOD | PATH | SERVICE CALLED | FRAUD_HOOK? | AUTH?
for every endpoint across:
  auth.py, transactions.py, goals.py, wealth.py, 
  insights.py, ai_chat.py, calendar.py

Flag any endpoint that:
- Is missing auth
- Is a write operation without a FRAUD_HOOK
- Has no response schema defined

Output as a markdown table. Fix any flagged issues.
```

### Step 3 — OpenAPI & Demo Convenience

Prompt:
```
Add these convenience endpoints to backend/main.py:

GET /demo/reset/{persona}
  Wipes and re-seeds data for persona (priya|ramesh|ananya)
  Returns {"message": "Demo reset for {persona}", "user_id": int}
  # Critical for demo day — judges will want to reset between personas
  # Protected by a DEMO_MODE env var (only works if DEMO_MODE=true)

GET /demo/personas
  Returns summary of all 3 personas with their user_ids
  # So the frontend knows which user_id to use per persona

Also add request/response logging middleware:
  Log: method, path, status_code, latency_ms, user_id (if authed)
  Write to a rotating file: logs/api.log
  # Useful for debugging on demo day
```

---

## VERIFY Checklist

- [ ] `POST /auth/login` returns `is_new_device: true` for unrecognized fingerprint
- [ ] Route audit table shows 0 unflagged write endpoints
- [ ] `GET /demo/reset/priya` only works with `DEMO_MODE=true`
- [ ] All 3 demo personas accessible via `/demo/personas`
- [ ] `GET /health` returns AI provider name
- [ ] Every router properly imported in `main.py`
