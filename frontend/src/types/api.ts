// frontend/src/types/api.ts

export type RiskAppetite = 'conservative' | 'moderate' | 'aggressive';
export type GoalHealthStatus = 'on_track' | 'at_risk' | 'off_track';
export type ActionImpactLevel = 'high' | 'medium' | 'low';
export type ActionUrgency = 'immediate' | 'this_week' | 'this_month';

export interface User {
  id: number;
  email: string;
  full_name: string;
  age: number;
  monthly_income: number;
  risk_appetite: RiskAppetite;
  is_kyc_verified: boolean;
  created_at: string;
  trusted_devices: string[];
}

export interface Transaction {
  id: number;
  user_id: number;
  txn_id: string;
  amount: number;
  type: 'debit' | 'credit';
  merchant_raw: string;
  merchant_normalized?: string;
  category: string;
  sub_category?: string;
  source: string;
  timestamp: string;
  balance_after?: number;
  description?: string;
  is_recurring: boolean;
  spending_personality_tag?: string;
}

export interface Investment {
  id: number;
  user_id: number;
  account_type: string;
  scheme_name: string;
  invested_amount: number;
  current_value: number;
  sip_amount?: number;
  returns_xirr?: number;
  interest_rate?: number;
  start_date?: string;
  maturity_date?: string;
}

export interface Asset {
  id: number;
  user_id: number;
  asset_type: string;
  name: string;
  purchase_value: number;
  current_value: number;
}

export interface GoalHealthResult {
  status: GoalHealthStatus;
  current_amount: number;
  target_amount: number;
  target_date: string;
  months_remaining: number;
  required_monthly: number;
  current_monthly: number;
  projected_completion_date: string;
  gap_amount: number;
}

export interface GoalConflict {
  conflicting_goals: string[];
  shortfall: number;
  message: string;
}

export interface GoalImpact {
  score: number;
  message: string;
}

export interface GoalStatus {
  id: number;
  name: string;
  health: GoalHealthResult;
}

export interface WealthSnapshot {
  user_id: number;
  snapshot_date: string;
  total_cash: number;
  total_investments: number;
  total_assets: number;
  total_liabilities: number;
  net_worth: number;
  net_worth_delta_mom: number;
  portfolio_health_score: number;
  financial_stress_score: number;
  investments: Investment[];
  assets: Asset[];
}

export interface WealthAction {
  action_id: string;
  title: string;
  description: string;
  action_type: string;
  impact_level: ActionImpactLevel;
  urgency: ActionUrgency;
  expected_impact_description: string;
  goal_impact_score?: number;
  data_payload?: any;
}

export interface CalendarEvent {
  event_id: string;
  event_type: string;
  event_date: string;
  title: string;
  amount: number;
  account_or_goal: string;
  is_critical: boolean;
  balance_warning?: string;
  action_suggestion?: string;
}

export interface SpendSummary {
  period_start: string;
  period_end: string;
  total_spend: number;
  total_income: number;
  savings_rate: number;
  by_category: Record<string, number>;
  top_merchants: { merchant: string; amount: number }[];
  mom_comparison: Record<string, number>;
}

export interface BehaviourProfile {
  weekend_vs_weekday_spend: number;
  month_start_vs_end_spend: {
    month_start_7d_avg: number;
    month_end_7d_avg: number;
    ratio: number;
  };
  impulse_spend_count: number;
  top_spending_personality?: string;
}

export interface StressScoreResult {
  score: number;
  level: string;
  top_signals: string[];
  trend: string;
}

export interface ScenarioResult {
  scenario_name: string;
  total_wealth_at_year_n: number;
  vs_base_case_delta: number;
  yearly_projections: { year: number; net_worth: number }[];
}

export interface MultiScenarioResult {
  scenarios: ScenarioResult[];
  chart_data: {
    x_axis: number[];
    series: { scenario_name: string; color: string; data: number[] }[];
  };
  cost_of_inaction: number;
  cost_of_inaction_message: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  assistant_message: string;
  referenced_actions?: WealthAction[];
  tokens_used: number;
}

export interface FraudCheckResult {
  fraud_check: 'STUB' | 'ACTIVE';
  status: 'pass' | 'warn' | 'block';
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high';
  message: string;
}

export interface APIError {
  detail: string;
}
