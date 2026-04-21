#!/bin/bash

# Create backend directories
mkdir -p backend/models
mkdir -p backend/schemas
mkdir -p backend/services
mkdir -p backend/routers
mkdir -p backend/fraud
mkdir -p backend/mock_data
mkdir -p backend/utils
mkdir -p backend/tests

# Create backend __init__.py files
touch backend/__init__.py
touch backend/models/__init__.py
touch backend/schemas/__init__.py
touch backend/services/__init__.py
touch backend/routers/__init__.py
touch backend/fraud/__init__.py
touch backend/mock_data/__init__.py
touch backend/utils/__init__.py
touch backend/tests/__init__.py

# Create backend empty files
touch backend/main.py
touch backend/config.py
touch backend/database.py
touch backend/services/ai_provider.py
touch backend/services/transaction_ingestor.py
touch backend/services/spend_lens.py
touch backend/services/behaviour_engine.py
touch backend/services/wealth_mapper.py
touch backend/services/goal_engine.py
touch backend/services/scenario_simulator.py
touch backend/services/strategy_engine.py
touch backend/services/insight_narrator.py
touch backend/services/financial_calendar.py
touch backend/routers/auth.py
touch backend/routers/transactions.py
touch backend/routers/investments.py
touch backend/routers/goals.py
touch backend/routers/wealth.py
touch backend/routers/insights.py
touch backend/routers/ai_chat.py
touch backend/routers/calendar.py
touch backend/fraud/hooks.py
touch backend/utils/merchant_normalizer.py
touch backend/utils/xirr.py
touch backend/utils/date_helpers.py
touch backend/tests/conftest.py
touch backend/tests/test_ingestor.py
touch backend/tests/test_spend_lens.py
touch backend/tests/test_goal_engine.py

# Create frontend directories
mkdir -p frontend/src/api
mkdir -p frontend/src/store
mkdir -p frontend/src/screens/Onboarding
mkdir -p frontend/src/screens/Dashboard
mkdir -p frontend/src/screens/Goals
mkdir -p frontend/src/screens/Portfolio
mkdir -p frontend/src/screens/Chat
mkdir -p frontend/src/screens/Settings
mkdir -p frontend/src/navigation
mkdir -p frontend/src/components
mkdir -p frontend/src/theme
mkdir -p frontend/src/types

# Create frontend empty files
touch frontend/app.config.ts
touch frontend/App.tsx
touch frontend/src/api/client.ts
touch frontend/src/api/endpoints.ts
touch frontend/src/store/useAuthStore.ts
touch frontend/src/store/useWealthStore.ts
touch frontend/src/store/useGoalStore.ts
touch frontend/src/screens/Onboarding/WelcomeScreen.tsx
touch frontend/src/screens/Onboarding/KYCScreen.tsx
touch frontend/src/screens/Onboarding/RiskQuizScreen.tsx
touch frontend/src/screens/Onboarding/GoalSetupScreen.tsx
touch frontend/src/screens/Dashboard/DashboardScreen.tsx
touch frontend/src/screens/Dashboard/NetWorthCard.tsx
touch frontend/src/screens/Dashboard/SpendingChart.tsx
touch frontend/src/screens/Dashboard/GoalProgressCard.tsx
touch frontend/src/screens/Goals/GoalsScreen.tsx
touch frontend/src/screens/Goals/GoalDetailScreen.tsx
touch frontend/src/screens/Goals/ScenarioSimScreen.tsx
touch frontend/src/screens/Portfolio/PortfolioScreen.tsx
touch frontend/src/screens/Portfolio/PortfolioHealthCard.tsx
touch frontend/src/screens/Chat/AIChatScreen.tsx
touch frontend/src/screens/Settings/SettingsScreen.tsx
touch frontend/src/navigation/RootNavigator.tsx
touch frontend/src/navigation/AppNavigator.tsx
touch frontend/src/navigation/OnboardingNavigator.tsx
touch frontend/src/components/WealthCard.tsx
touch frontend/src/components/ActionCard.tsx
touch frontend/src/components/RiskBadge.tsx
touch frontend/src/components/SkeletonLoader.tsx
touch frontend/src/components/FraudWarningModal.tsx
touch frontend/src/theme/colors.ts
touch frontend/src/theme/typography.ts
touch frontend/src/theme/spacing.ts
touch frontend/src/types/api.ts
touch frontend/src/types/navigation.ts

echo "Folder structure created successfully."
