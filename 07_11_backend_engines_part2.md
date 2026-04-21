# Workflow 07 — Goal Engine

**Goal:** Build goal tracking with health status, conflict detection, and the "Goal Impact Score" for wealth actions.

**Prerequisites:** Workflows 03–06 complete. WealthSnapshot working.

---

## Context to Paste

```
@file: backend/models/goal.py
@file: backend/schemas/goal.py
@file: backend/schemas/wealth_snapshot.py
@file: backend/services/wealth_mapper.py
```

---

## STEPS

### Step 1 — Goal Engine Service

Prompt:
```
Write backend/services/goal_engine.py

class GoalEngine:

  def get_goal_health(self, goal: Goal, 
                      monthly_savings: float) -> GoalHealthResult:
    """
    GoalHealthResult:
      status: "on_track" | "at_risk" | "off_track"
      current_amount: float
      target_amount: float
      target_date: date
      months_remaining: int
      required_monthly: float  # what's needed to hit goal on time
      current_monthly: float   # what user is actually saving toward this goal
      projected_completion_date: date  # at current rate, when will they hit it?
      gap_amount: float  # how much short per month
      
    Logic:
      on_track: projected_completion_date <= target_date
      at_risk: projected_completion_date is 1-6 months late
      off_track: projected_completion_date is 6+ months late OR current_monthly=0
    """

  def detect_goal_conflicts(self, user_id: int, 
                             goals: list[Goal]) -> list[GoalConflict]:
    """
    Identify when two or more goals compete for the same money.
    
    total_required_monthly = sum(goal.required_monthly for all active goals)
    available_monthly = monthly_income - fixed_expenses - current_savings
    
    If total_required_monthly > available_monthly * 1.1:
      Return GoalConflict with:
        - conflicting_goals: list of goal names
        - shortfall: float
        - message: "You need ₹X/month for all goals but only ₹Y is available. 
                    Prioritize which matters most."
    """

  def compute_goal_impact_score(self, action: WealthAction, 
                                 goal: Goal,
                                 current_monthly_savings: float) -> float:
    """
    How much does this action move the needle on this goal?
    Returns a score 0.0 - 1.0 and a human sentence.
    
    Example: Starting ₹5,000 SIP when goal needs ₹4,500/month:
      score = 0.9, message = "This SIP alone covers 90% of your Home goal's 
                              monthly requirement — moves it from At Risk → On Track"
    """

  def get_all_goal_statuses(self, user_id: int) -> list[GoalStatus]:
    """Compute health for all user goals. Used by dashboard."""
```

### Step 2 — Goals Router

Prompt:
```
Write backend/routers/goals.py

  GET  /goals                    → list[GoalStatus]
  POST /goals                    → create goal, returns GoalStatus
  GET  /goals/{id}               → GoalStatus (detailed)
  PUT  /goals/{id}               → update goal
  DELETE /goals/{id}             → delete goal
  GET  /goals/conflicts          → list[GoalConflict]
  GET  /goals/{id}/impact/{action_type}  → GoalImpactScore

All write endpoints: call run_full_fraud_check() stub # FRAUD_HOOK
```

---

## VERIFY Checklist

- [ ] Priya's Emergency Fund goal: on_track (saving ₹5,000/month, needs ₹2,500)
- [ ] Ananya has no goals → conflicts endpoint returns [] with a nudge to create goals
- [ ] Conflict detected if Ramesh tries to fully fund both goals simultaneously
- [ ] GoalImpactScore returns a human sentence, not just a number

---

# Workflow 08 — Scenario Simulator

**Goal:** Build the interactive what-if projection engine. This is a high-scoring visual feature for demos.

**Prerequisites:** Workflow 07 complete. GoalEngine working.

---

## Context to Paste

```
@file: backend/services/goal_engine.py
@file: backend/services/wealth_mapper.py
@file: backend/utils/xirr.py
```

---

## STEPS

### Step 1 — Projection Engine

Prompt:
```
Write backend/services/scenario_simulator.py

class ScenarioSimulator:

  def run_scenario(self, user_id: int, scenario: ScenarioInput) -> ScenarioResult:
    """
    ScenarioInput:
      base_monthly_savings: float  # current savings rate
      adjustments: list[Adjustment]
        Adjustment: type (increase_sip | reduce_spend | add_lump_sum | 
                          change_income), amount: float, category: str | None
      projection_years: int  # 5, 10, or 20
      goal_id: int | None  # if set, also show goal completion date
    
    ScenarioResult:
      scenario_name: str
      yearly_projections: list[YearlyProjection]
        YearlyProjection: year, net_worth, invested, returns_earned
      goal_completion_date: date | None
      total_wealth_at_year_n: float
      vs_base_case_delta: float  # how much better/worse vs doing nothing
    """

  def run_multi_scenario(self, user_id: int, 
                          scenarios: list[ScenarioInput]) -> MultiScenarioResult:
    """
    Run up to 4 scenarios in parallel and return all results.
    Always include a "What if nothing changes?" base case as scenario[0].
    
    MultiScenarioResult:
      scenarios: list[ScenarioResult]
      chart_data: ChartData  # formatted for Victory Native on frontend
        ChartData:
          x_axis: list[int]  # years
          series: list[ChartSeries]
            ChartSeries: scenario_name, color, data: list[float]
      cost_of_inaction: float  # base_case final wealth vs best scenario
      cost_of_inaction_message: str
        # "Doing nothing costs you ₹X over 10 years compared to your best option"
    """

  def _project_wealth(self, starting_wealth: float, monthly_savings: float,
                       annual_return_rate: float, years: int) -> list[float]:
    """
    Compound growth projection with monthly contributions.
    Use 8% default annual return for equity, 6.5% for conservative.
    Apply inflation adjustment at 6% for real-value display.
    """
```

### Step 2 — Simulator Router

Prompt:
```
Add to backend/routers/wealth.py or create routers/simulation.py:

  POST /simulate/single     → ScenarioResult
  POST /simulate/multi      → MultiScenarioResult
  GET  /simulate/presets/{user_id}  → list[PresetScenario]
    # 3 pre-built scenarios based on user's actual data:
    # "Increase your SIP by ₹1,000", "Cut dining spend by 30%", 
    # "Add a ₹50,000 lump sum today"
```

---

## VERIFY Checklist

- [ ] Base case "nothing changes" is always scenario[0]
- [ ] cost_of_inaction_message is populated and human-readable
- [ ] chart_data.series has correct color assignments (defined in theme)
- [ ] Projection with 0 savings still runs without ZeroDivisionError
- [ ] Priya's "Increase SIP by ₹1,000" scenario moves Home goal forward by ~8 months

---

# Workflow 09 — Strategy Engine

**Goal:** Build the ranked Wealth Actions system — the core output of the intelligence layer.

**Prerequisites:** Workflows 05–08 all complete.

---

## Context to Paste

```
@file: backend/schemas/action.py
@file: backend/services/behaviour_engine.py
@file: backend/services/wealth_mapper.py
@file: backend/services/goal_engine.py
```

---

## STEPS

### Step 1 — Strategy Engine Service

Prompt:
```
Write backend/services/strategy_engine.py

class StrategyEngine:

  def generate_wealth_actions(self, user_id: int) -> list[WealthAction]:
    """
    The main output of the intelligence layer.
    
    Pull inputs from:
      - WealthMapper.get_wealth_snapshot()
      - BehaviourEngine.compute_behaviour_profile()
      - BehaviourEngine.detect_anomalies()
      - GoalEngine.get_all_goal_statuses()
      - SpendLens.detect_overspend()
    
    Apply these rule sets to generate WealthAction objects:
    
    RULE SET 1 — Cash Drag:
      If cash > 6x monthly_expense → "Move excess cash to liquid fund"
      Impact: high, Urgency: this_week
    
    RULE SET 2 — FD Maturity:
      If any FD matures in ≤ 14 days → "Your FD matures soon — plan reinvestment"
      Impact: high, Urgency: immediate
    
    RULE SET 3 — Tax Saving:
      If current month is Jan/Feb/Mar AND user has no ELSS → 
        "Tax season: consider ELSS for 80C benefit"
      Impact: high, Urgency: immediate
    
    RULE SET 4 — Overspend → Redirect:
      For each overspend alert from SpendLens:
        "You spent ₹X extra on {category}. Redirect to {lowest_health_goal}"
      Impact: medium, Urgency: this_month
    
    RULE SET 5 — Goal at Risk:
      For each goal with status=at_risk:
        "Increase monthly contribution by ₹X to get {goal} back on track"
      Impact: high, Urgency: this_week
    
    RULE SET 6 — No Emergency Fund:
      If user has no emergency fund goal OR cash < 1x monthly_expense:
        "Build a 3-month emergency buffer before investing"
      Impact: high, Urgency: immediate
    
    RULE SET 7 — Portfolio Diversification:
      If portfolio_health_score < 40 AND user has only one investment type:
        "Diversify: add a {suggested_type} to reduce concentration risk"
      Impact: medium, Urgency: this_month
    
    RULE SET 8 — Savings Rate Declining:
      If savings_rate_trend shows 3 consecutive months of decline:
        "Your savings rate has dropped {X}% in 3 months — review your spending"
      Impact: high, Urgency: this_week
    
    Sort output by: urgency (immediate first) then impact (high first).
    Deduplicate — don't show 2 actions about the same issue.
    Limit to top 5 actions to avoid overwhelming the user.
    
    Each action must have goal_impact_score if it relates to a goal.
    """

  def quantify_habit_roi(self, user_id: int, 
                          category: str, 
                          reduction_pct: float) -> HabitROIResult:
    """
    "If you reduce {category} spend by {pct}%, here is the exact impact."
    
    HabitROIResult:
      monthly_savings_freed: float
      yearly_savings_freed: float
      goal_acceleration: dict[str, str]  # goal_name → "X months sooner"
      10_year_wealth_impact: float
      message: str  # single punchy sentence
        # "Cutting dining by 30% frees ₹1,920/month — 
        #  your Emergency Fund goal arrives 4 months sooner"
    """
```

### Step 2 — Insights Router

Prompt:
```
Write backend/routers/insights.py

  GET /insights/actions               → list[WealthAction] (top 5)
  GET /insights/actions/all           → list[WealthAction] (all, paginated)
  GET /insights/habit-roi/{category}?reduction_pct=30  → HabitROIResult
  GET /insights/summary               → InsightsSummary
    InsightsSummary:
      portfolio_health_score, stress_score, top_action: WealthAction,
      goal_summary: list[{name, status, pct_complete}]
```

---

## VERIFY Checklist

- [ ] Ananya gets "Build emergency buffer" as action[0] (highest urgency)
- [ ] Ramesh gets FD maturity alert if his FD matures in next 14 days
- [ ] Actions list never exceeds 5 items
- [ ] `quantify_habit_roi("FOOD", 0.3)` for Priya returns non-zero values
- [ ] All actions have valid `data_payload` for frontend deep-linking

---

# Workflow 10 — Insight Narrator

**Goal:** Build the explainability layer that converts engine outputs into plain language. This is what judges will specifically look for.

**Prerequisites:** Workflows 03–09 complete.

---

## Context to Paste

```
@file: backend/services/strategy_engine.py
@file: backend/services/behaviour_engine.py
@file: backend/schemas/action.py
```

---

## STEPS

### Step 1 — Template-Based Narrator (No LLM)

Prompt:
```
Write backend/services/insight_narrator.py

Part 1: Rule-templated narrator (no LLM required — works offline).

class InsightNarrator:

  TEMPLATES = {
    "overspend": "Your spending on {category} (₹{current:,.0f}) is {pct:.0f}% above "
                 "your {period}-month average of ₹{average:,.0f}. "
                 "This is the main reason your savings rate {impact}.",
    "goal_at_risk": "At your current savings rate, you'll reach your {goal_name} goal "
                    "{months_late} months late (by {projected_date}). "
                    "Adding ₹{gap:,.0f}/month puts it back on track.",
    "stress_score": "Your financial stress score is {level} ({score}/100). "
                    "Main contributors: {top_signals_joined}.",
    "portfolio_health": "Your portfolio health is {score}/100. "
                        "Strongest area: {best_factor}. "
                        "Biggest gap: {worst_factor}.",
    "wealth_action": "{action_title}. {expected_impact_description}",
    "habit_roi": "Cutting {category} spend by {pct:.0f}% frees ₹{freed:,.0f}/month — "
                 "{goal_acceleration_str}.",
    "cost_of_inaction": "Maintaining current habits, your net worth reaches "
                        "₹{base:,.0f} in {years} years. "
                        "Your best scenario reaches ₹{best:,.0f} — "
                        "a ₹{delta:,.0f} difference.",
  }

  def narrate(self, template_key: str, **kwargs) -> str:
    """Fill a template with kwargs. Raise if template not found."""

  def narrate_action(self, action: WealthAction) -> str:
    """Produce a 2-sentence explanation for a WealthAction."""

  def narrate_weekly_summary(self, user_id: int) -> WeeklySummary:
    """
    3-5 sentence summary of the user's financial week.
    WeeklySummary: headline, body, positive_note, top_action_cta
    headline example: "You saved 18% this week — your best rate in 2 months"
    positive_note: always end on something the user did right (even if small)
    """
```

### Step 2 — LLM-Enhanced Narrator (Bonus Layer)

Prompt:
```
Add to backend/services/insight_narrator.py:

  async def narrate_with_ai(self, context: NarratorContext, 
                             tone: str = "friendly") -> str:
    """
    Call AI provider (Claude or Gemini) to produce a richer explanation.
    
    NarratorContext:
      template_key: str
      template_output: str  # the rule-based version (always computed first)
      raw_data: dict         # the numbers behind the insight
      user_name: str
      user_risk_appetite: str
    
    Prompt strategy (token-efficient):
      - Pass the rule-based output as a starting point
      - Ask the LLM to ONLY rewrite it in a warmer tone — not to re-analyze
      - Limit response to 3 sentences max
      - Use AI_PROVIDER toggle from ai_provider.py
    
    Fallback: if AI call fails, return template_output silently.
    
    Token budget: max_tokens=150 per call. This is a rewrite task, not analysis.
    """
```

---

## VERIFY Checklist

- [ ] All templates fill without KeyError for valid inputs
- [ ] `narrate_weekly_summary` always has a positive_note
- [ ] `narrate_with_ai` falls back to template on API error
- [ ] max_tokens=150 hardcoded in the AI call (not configurable)
- [ ] LLM prompt is < 200 tokens (pass only what's needed)

---

# Workflow 11 — Financial Calendar

**Goal:** Build the upcoming events layer — SIP debits, FD maturities, EMI due dates. Small feature, high demo visibility.

**Prerequisites:** Workflow 06 (Wealth Mapper) complete.

---

## Context to Paste

```
@file: backend/models/investment.py
@file: backend/models/transaction.py
```

---

## STEPS

### Step 1 — Calendar Service

Prompt:
```
Write backend/services/financial_calendar.py

class FinancialCalendar:

  def get_upcoming_events(self, user_id: int, 
                           days_ahead: int = 30) -> list[CalendarEvent]:
    """
    CalendarEvent:
      event_id, event_type (sip_debit | fd_maturity | rd_installment | 
                             emi_due | salary_expected | goal_review),
      event_date: date,
      title: str,
      amount: float,
      account_or_goal: str,
      is_critical: bool,  # True if user might not have enough balance
      balance_warning: str | None,
      action_suggestion: str | None

    Detection logic:
      SIP debits: from investment.sip_date + sip_frequency, next N occurrences
      FD maturities: investment.maturity_date within days_ahead
      Salary expected: infer from last 3 salary credits — predict next date
      EMI due: detect recurring debit patterns (same merchant, similar amount, monthly)
    
    Balance warning: if event_amount > current_balance * 0.8:
      is_critical = True
      balance_warning = "Your ₹{amount} SIP debits in {days} days. 
                         Current balance: ₹{balance} — keep a buffer."
    """

  def get_monthly_calendar(self, user_id: int, 
                            month: int, year: int) -> MonthlyCalendar:
    """
    MonthlyCalendar:
      month, year,
      events_by_day: dict[int, list[CalendarEvent]]  # day → events
      total_outflows: float,
      total_expected_inflows: float,
      net_cash_flow_projected: float
    """

Add to backend/routers/calendar.py:
  GET /calendar/upcoming?days=30    → list[CalendarEvent]
  GET /calendar/month?month=3&year=2025  → MonthlyCalendar
```

---

## VERIFY Checklist

- [ ] Priya's SIP shows up in calendar 5 days before debit date
- [ ] Ramesh's FD maturity shows up with action_suggestion (reinvest recommendation)
- [ ] Balance warning fires if projected balance < event amount
- [ ] Salary prediction works from last 3 month salary credits
