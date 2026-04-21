// frontend/src/types/navigation.ts
export type RootStackParamList = {
  Onboarding: undefined;
  App: undefined;
};

export type OnboardingStackParamList = {
  Welcome: undefined;
  KYC: undefined;
  RiskQuiz: undefined;
  GoalSetup: undefined;
};

export type AppTabParamList = {
  Dashboard: undefined;
  Goals: undefined;
  Portfolio: undefined;
  Chat: undefined;
};

export type GoalsStackParamList = {
  GoalsList: undefined;
  GoalDetail: { goalId: number };
  ScenarioSim: { goalId?: number };
};
