# Workflow 14 — React Native Scaffold

**Goal:** Set up the Expo project, navigation structure, shared components, and design system. The visual foundation everything else renders on.

**Estimated tokens:** Medium. Focus is structure and theme, not heavy logic.

**Prerequisites:** Workflow 01 (frontend folder structure), backend running on localhost:8000.

---

## Context to Paste

```
@file: frontend/src/theme/colors.ts
@file: frontend/src/theme/typography.ts
@file: frontend/src/api/client.ts
@file: frontend/src/types/api.ts
```

---

## STEPS

### Step 1 — API Types

Prompt:
```
Write frontend/src/types/api.ts

TypeScript interfaces mirroring all backend Pydantic schemas:
  User, Transaction, Investment, Asset, Goal, GoalStatus, 
  WealthSnapshot, WealthAction, CalendarEvent,
  SpendSummary, BehaviourProfile, StressScoreResult,
  ScenarioResult, MultiScenarioResult, ChartData,
  ChatMessage, ChatRequest, ChatResponse,
  FraudCheckResult  # STUB type — always has fraud_check: "STUB"

Also define:
  APIError: { detail: string, status_code: number }
  PaginatedResponse<T>: { items: T[], total: number, page: number }
```

### Step 2 — Zustand Stores

Prompt:
```
Write the Zustand stores:

frontend/src/store/useAuthStore.ts
  state: user: User | null, token: string | null, isLoading: bool
  actions: login(email, password, deviceFingerprint), 
           logout(), 
           loadFromStorage()  # restore token from SecureStore on app start

frontend/src/store/useWealthStore.ts
  state: snapshot: WealthSnapshot | null, actions: WealthAction[],
         isLoading: bool, lastFetched: Date | null
  actions: fetchSnapshot(), fetchActions(), refresh()
  
frontend/src/store/useGoalStore.ts
  state: goals: GoalStatus[], conflicts: GoalConflict[], isLoading: bool
  actions: fetchGoals(), createGoal(data), updateGoal(id, data)

All stores: 
  - Use React Query for server state, Zustand only for truly global client state
  - Invalidate React Query cache on relevant mutations
```

### Step 3 — Navigation

Prompt:
```
Write frontend/src/navigation/RootNavigator.tsx

Navigation structure:
  RootNavigator
    ├── OnboardingNavigator (if !user.is_kyc_verified)
    │     ├── WelcomeScreen
    │     ├── KYCScreen
    │     ├── RiskQuizScreen
    │     └── GoalSetupScreen
    └── AppNavigator (authenticated)
          ├── BottomTabNavigator
          │     ├── DashboardStack → DashboardScreen
          │     ├── GoalsStack → GoalsScreen → GoalDetailScreen → ScenarioSimScreen
          │     ├── PortfolioStack → PortfolioScreen
          │     └── ChatStack → AIChatScreen
          └── Modal screens (presented over tabs):
                ├── FraudWarningModal  # STUB — renders nothing
                └── SettingsScreen

Tab bar icons: use @expo/vector-icons Ionicons
  Dashboard: home-outline, Goals: flag-outline, 
  Portfolio: pie-chart-outline, Chat: chatbubble-outline
Tab bar style: use theme colors (deep navy background, teal active)

TypeScript: define all navigation param lists in frontend/src/types/navigation.ts
```

### Step 4 — Shared Components

Prompt:
```
Write these reusable components. Each file: frontend/src/components/<name>.tsx

WealthCard.tsx
  Props: title, value (₹ formatted), subtitle?, trend?: "up"|"down"|"neutral",
         trendValue?: string, onPress?: () => void
  Style: rounded card, deep navy bg, gold value text, teal trend indicator
  Include a skeleton loading variant

ActionCard.tsx
  Props: action: WealthAction, onPress: () => void, onDismiss?: () => void
  Style: left colored border (red=immediate, amber=this_week, green=this_month)
  Show: title, description (truncated to 2 lines), impact badge, urgency pill
  Swipe-to-dismiss gesture using PanResponder

RiskBadge.tsx  
  Props: level: "low"|"medium"|"high", size?: "sm"|"md"
  Style: pill shape, green/amber/red matching level

SkeletonLoader.tsx
  Props: width, height, borderRadius?
  Animated shimmer effect using Animated API
  Export: SkeletonCard, SkeletonText, SkeletonAvatar variants

FraudWarningModal.tsx  # FRAUD_HOOK: renders stub warning for now
  Props: visible: bool, onConfirm: () => void, onCancel: () => void,
         riskLevel: "low"|"medium"|"high", message?: string
  Current behavior: if riskLevel is "low" → auto-confirm, don't show modal
  medium/high → show a simple "Are you sure?" modal (placeholder)
  # Full fraud UI implemented when cybersecurity layer is added
  Comment at top: // FRAUD_HOOK: This modal will be replaced with full fraud UI
```

---

## VERIFY Checklist

- [ ] `expo start` launches without TypeScript errors
- [ ] Navigation moves from Onboarding → App flow when user logs in
- [ ] WealthCard renders with skeleton while loading
- [ ] FraudWarningModal has FRAUD_HOOK comment at top
- [ ] All API types compile — no `any` types except explicitly marked

---

# Workflow 15 — Dashboard Screen

**Goal:** Build the main dashboard — the first thing users see after login. This is the highest-visibility screen for judges.

**Prerequisites:** Workflow 14 complete. Backend /wealth/snapshot and /insights/summary endpoints working.

---

## Context to Paste

```
@file: frontend/src/components/WealthCard.tsx
@file: frontend/src/components/ActionCard.tsx
@file: frontend/src/store/useWealthStore.ts
@file: frontend/src/theme/colors.ts
@file: frontend/src/types/api.ts (WealthSnapshot, WealthAction, SpendSummary)
```

---

## STEPS

### Step 1 — Dashboard Screen

Prompt:
```
Write frontend/src/screens/Dashboard/DashboardScreen.tsx

Layout (ScrollView, vertically stacked):

1. Header bar
   - "Good morning, {name}" greeting (time-based: morning/afternoon/evening)
   - Small avatar placeholder (initials)
   - Bell icon for notifications

2. Net Worth Hero Card (full width)
   - Large ₹-formatted net worth number (Playfair Display font, 36sp)
   - Month-on-month delta: "↑ ₹12,400 from last month" (green) or "↓" (red)
   - Portfolio Health Score: circular progress ring 0-100 with color gradient
   - Tap → navigates to PortfolioScreen

3. Quick Stats Row (3 equal cards side by side)
   - This month's savings rate (%)
   - Financial stress score (Low/Moderate/High)  
   - Goals on track (X/Y)

4. Spending Chart
   - Component: SpendingChart.tsx (see Step 2)
   - Title: "This month's spending"

5. Top Wealth Actions (section title + 3 ActionCards)
   - "Your Action Plan" header
   - Top 3 WealthActions from /insights/actions
   - "See all" link → not yet implemented (TODO)

6. Goal Progress Cards (horizontal scroll)
   - Component: GoalProgressCard.tsx (see Step 2)
   - One card per active goal

Data fetching:
  - Use React Query: useQuery(['wealth-snapshot'], fetchWealthSnapshot)
  - useQuery(['insights-actions'], fetchInsightActions)
  - useQuery(['goals'], fetchGoals)
  - Show SkeletonLoader while loading
  - Pull-to-refresh on the ScrollView

Style notes:
  - Background: deep navy (#0A1628)
  - Cards: slightly lighter navy (#0F1F3D) with subtle border
  - All money values: DM Sans Bold or Playfair Display
  - Maintain 16dp horizontal padding throughout
```

### Step 2 — Chart Components

Prompt:
```
Write frontend/src/screens/Dashboard/SpendingChart.tsx
  
Using Victory Native (VictoryPie or VictoryBar — your choice, use what renders better):
  
Props: 
  data: {category: string, amount: number, color: string}[]
  period: string  # "March 2025"

Features:
  - Donut chart showing category breakdown
  - Tap a slice → highlight + show category name + amount in center
  - Legend below chart (category name + ₹ amount, color coded)
  - Animated on mount (Animated.spring)
  - If data is empty → empty state: "No spending data yet"

Colors per category (use theme):
  FOOD: "#FF6B6B", TRANSPORT: "#4ECDC4", SHOPPING: "#45B7D1",
  UTILITIES: "#96CEB4", ENTERTAINMENT: "#FFEAA7", EMI: "#DDA0DD",
  OTHER: "#999999"

Write frontend/src/screens/Dashboard/GoalProgressCard.tsx

Props: goal: GoalStatus, onPress: () => void

Card shows:
  - Goal name (bold)
  - Progress bar (teal fill on grey track) — current_amount / target_amount
  - "₹X of ₹Y" text below bar
  - Status pill: On Track (green) / At Risk (amber) / Off Track (red)
  - Months remaining or projected_completion_date
  - Width: 200dp (for horizontal scroll), height: 120dp
```

### Step 3 — Onboarding Screens

Prompt:
```
Write the 4 onboarding screens. Keep them clean and fast.

frontend/src/screens/Onboarding/WelcomeScreen.tsx
  - SecureWealth Twin logo/wordmark (text-based, styled)
  - 3 feature highlights with icons (Grow wealth, Track spending, Stay safe)
  - "Get Started" button → KYCScreen
  - "I have an account" link → login

frontend/src/screens/Onboarding/KYCScreen.tsx
  - Form: full_name, email, password, age, monthly_income, PAN (optional)
  - Inline validation (no submit until valid)
  - "Simulation only — no real KYC" disclaimer at bottom
  - On submit: POST /auth/register, then → RiskQuizScreen

frontend/src/screens/Onboarding/RiskQuizScreen.tsx
  - 5 simple questions to determine risk appetite
  - Each question: 3 option cards (conservative/moderate/aggressive mapped)
  - Progress bar at top
  - On complete: store result, → GoalSetupScreen

frontend/src/screens/Onboarding/GoalSetupScreen.tsx
  - "What are you saving for?" — 6 goal type buttons with icons
    (Home, Education, Retirement, Emergency Fund, Vehicle, Other)
  - Select multiple
  - For each selected: modal to enter target amount + target date
  - "Skip for now" link
  - On complete: POST /goals for each, then → Dashboard
```

---

## VERIFY Checklist

- [ ] Dashboard loads Priya's data — net worth, 3 actions, goal cards visible
- [ ] Spending donut chart renders with correct category colors
- [ ] Pull-to-refresh triggers React Query refetch
- [ ] Goal cards scroll horizontally without overflow
- [ ] Onboarding flow: Welcome → KYC → Quiz → Goals → Dashboard without errors
- [ ] All SkeletonLoaders show while queries are loading

---

# Workflow 16 — Goals & Scenario Simulator Screens

**Goal:** Build the goal tracking and interactive what-if simulator screens.

**Prerequisites:** Workflows 14–15 complete. Goal Engine and Scenario Simulator APIs working.

---

## Context to Paste

```
@file: frontend/src/types/api.ts (GoalStatus, ScenarioResult, MultiScenarioResult)
@file: frontend/src/store/useGoalStore.ts
@file: frontend/src/theme/colors.ts
```

---

## STEPS

### Step 1 — Goals Screen

Prompt:
```
Write frontend/src/screens/Goals/GoalsScreen.tsx

Layout:
  1. Header: "Your Goals" + "+" button to add new goal
  
  2. Conflict banner (if any conflicts):
     Amber background card: "⚠ Two goals are competing for the same funds"
     "Resolve" button → shows conflict detail modal
  
  3. Goals list (FlatList):
     Each item: expanded GoalProgressCard with:
       - Progress bar
       - Status pill
       - Required monthly vs current monthly (two values side by side)
       - "Simulate" button → ScenarioSimScreen
       - Chevron → GoalDetailScreen
  
  4. Empty state (Ananya): illustrated card "Set your first goal"
     with "Get started" button

Write frontend/src/screens/Goals/GoalDetailScreen.tsx
  Full detail of one goal:
  - Progress visualization (large ring chart, not bar)
  - Timeline: created_date → today marker → target_date on a horizontal line
  - "Projected completion" date (colored red if late)
  - Required monthly saving + current actual (gap highlighted if negative)
  - "Run Scenario" button → ScenarioSimScreen
  - Edit goal button → inline edit form
```

### Step 2 — Scenario Simulator Screen

Prompt:
```
Write frontend/src/screens/Goals/ScenarioSimScreen.tsx

This is the interactive what-if projector.

Layout:
  1. Title: "What if...?" header

  2. Adjustment Sliders (3 rows):
     - "Increase monthly SIP by" — slider ₹0 to ₹10,000 (step ₹500)
     - "Reduce {top_spending_category} spend by" — slider 0% to 50%
     - "Add lump sum today" — slider ₹0 to ₹1,00,000 (step ₹5,000)
     Below sliders: "vs. doing nothing" toggle to show/hide base case

  3. Projection Chart (Victory Native line chart):
     X axis: years (0 to 10 or 20 — toggle)
     Y axis: net worth in ₹ lakhs
     Lines: one per scenario (max 4), colored from theme
     "What if nothing changes?" line always shown as dashed grey
     Animate chart redraw when sliders change (debounce 400ms)

  4. Key Metrics Row (updates live with sliders):
     - Net worth at year 10: ₹X
     - Goal completion: [date] (or "X months sooner")
     - Cost of inaction: "Doing nothing costs you ₹X"

  5. "Save this scenario" button (shows a name input → stores locally)

Data: call POST /simulate/multi on slider change (debounced).
Show loading spinner on chart during API call.
```

---

## VERIFY Checklist

- [ ] Conflict banner appears for Ramesh (2 competing goals)
- [ ] Simulator chart animates when sliders move
- [ ] Cost of inaction message updates live
- [ ] Base case "nothing changes" always visible as dashed line
- [ ] Empty state renders correctly for Ananya (no goals)

---

# Workflow 17 — Portfolio Screen

**Goal:** Build the investment tracker and portfolio health screens.

**Prerequisites:** Workflow 14 complete. Wealth Mapper API working.

---

## STEPS

### Step 1 — Portfolio Screen

Prompt:
```
Write frontend/src/screens/Portfolio/PortfolioScreen.tsx

Layout:
  1. Portfolio Health Score (large, centered)
     Circular gauge 0-100 with color: red<40, amber 40-70, green>70
     Below: breakdown bars for each factor (Diversification, Returns, 
     Goal Alignment, Emergency Buffer) — thin horizontal bars with labels

  2. Summary row: Total Invested | Current Value | Overall Return%
     Three equal width stat boxes, values in large text

  3. Investment list (FlatList, grouped by type):
     Section headers: "Mutual Funds", "Fixed Deposits", "Other"
     Each investment card:
       - Scheme name (truncated)
       - Invested: ₹X → Current: ₹Y (with arrow and color)
       - Return%: absolute + XIRR
       - For SIPs: next debit date pill

  4. Underperforming flags (if any):
     Amber banner per flag: e.g., "Your FD rate may not beat inflation"

  5. Assets section (collapsible):
     Gold, Property, Vehicle cards with current value

  6. Empty state (Ananya):
     "No investments yet" with ActionCard for "Start your first SIP"

Data: useQuery(['wealth-investments'], fetchInvestmentSummary)
      useQuery(['wealth-snapshot'], fetchWealthSnapshot)
```

---

## VERIFY Checklist

- [ ] Ramesh has the highest portfolio health score of the 3 personas
- [ ] Underperforming flag renders if any FD rate < 6.5%
- [ ] Ananya sees empty state with starter action
- [ ] Return percentage colored green (positive) or red (negative)

---

# Workflow 18 — AI Chat Screen

**Goal:** Build the conversational AI screen with suggested questions, rich responses, and action deep-links.

**Prerequisites:** Workflow 12 (AI provider + chat router) complete.

---

## STEPS

### Step 1 — Chat Screen

Prompt:
```
Write frontend/src/screens/Chat/AIChatScreen.tsx

Layout:
  1. Header: "Your Wealth Advisor" + provider badge (Claude/Gemini — 
     shows which AI is active, read from /health endpoint)

  2. Suggested Questions bar (horizontal scroll, above input):
     Chips from GET /chat/suggested-questions
     Tap → fills input and sends immediately
     Refresh icon to reload suggestions

  3. Chat messages (FlatList, inverted for bottom-to-top scroll):
     User messages: right-aligned, teal background
     Assistant messages: left-aligned, dark card
     For assistant messages: also show referenced WealthActions below message
       as tappable ActionCard stubs (navigate to relevant screen)
     Typing indicator (3 animated dots) while waiting for response

  4. Input bar (bottom, above keyboard):
     TextInput (multiline, max 3 lines)
     Send button (disabled when empty or loading)
     Character counter (max 500)

State management:
  - Keep conversation_history in local component state (not persisted)
  - Trim to last 6 messages before each API call
  - On unmount: warn "Chat history will be cleared" (local only, by design)

Special behaviors:
  - If assistant message contains a WealthAction reference:
    render an ActionCard below the text with "View details →"
  - First message in every session: show welcome message with user's name
    and their current stress score level (fetched from /behaviour/stress-score)
```

---

## VERIFY Checklist

- [ ] Provider badge shows "Claude" or "Gemini" correctly
- [ ] Suggested questions chip → auto-sends
- [ ] History is trimmed to 6 messages before API call (check Network tab)
- [ ] Referenced WealthActions render as tappable cards below message
- [ ] Typing indicator shows while awaiting API response
