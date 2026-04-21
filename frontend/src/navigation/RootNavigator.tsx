// frontend/src/navigation/RootNavigator.tsx
import React, { useEffect } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Ionicons } from "@expo/vector-icons";
import { useAuthStore } from "../store/useAuthStore";
import { colors } from "../theme/colors";

// Screens (stubs)
import WelcomeScreen from "../screens/Onboarding/WelcomeScreen";
import KYCScreen from "../screens/Onboarding/KYCScreen";
import RiskQuizScreen from "../screens/Onboarding/RiskQuizScreen";
import GoalSetupScreen from "../screens/Onboarding/GoalSetupScreen";
import DashboardScreen from "../screens/Dashboard/DashboardScreen";
import GoalsScreen from "../screens/Goals/GoalsScreen";
import PortfolioScreen from "../screens/Portfolio/PortfolioScreen";
import AIChatScreen from "../screens/Chat/AIChatScreen";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const OnboardingNavigator = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Welcome" component={WelcomeScreen} />
    <Stack.Screen name="KYC" component={KYCScreen} />
    <Stack.Screen name="RiskQuiz" component={RiskQuizScreen} />
    <Stack.Screen name="GoalSetup" component={GoalSetupScreen} />
  </Stack.Navigator>
);

const AppNavigator = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      headerShown: false,
      tabBarIcon: ({ focused, color, size }) => {
        let iconName: any = "help-outline";
        if (route.name === "Dashboard") iconName = focused ? "home" : "home-outline";
        else if (route.name === "Goals") iconName = focused ? "flag" : "flag-outline";
        else if (route.name === "Portfolio") iconName = focused ? "pie-chart" : "pie-chart-outline";
        else if (route.name === "Chat") iconName = focused ? "chatbubble" : "chatbubble-outline";
        return <Ionicons name={iconName} size={size} color={color} />;
      },
      tabBarActiveTintColor: colors.accent,
      tabBarInactiveTintColor: 'rgba(242, 237, 228, 0.4)',
      tabBarStyle: { 
        backgroundColor: 'rgba(8, 12, 20, 0.95)',
        position: 'absolute',
        borderTopWidth: 1,
        borderTopColor: 'rgba(255, 255, 255, 0.05)',
        height: 90,
        paddingTop: 10,
        paddingBottom: 30,
        elevation: 0,
        shadowOpacity: 0,
      },
      tabBarLabelStyle: {
        fontSize: 10,
        fontWeight: 'bold',
        textTransform: 'uppercase',
        letterSpacing: 1.5,
        marginTop: 5,
      },
    })}
  >
    <Tab.Screen name="Dashboard" component={DashboardScreen} />
    <Tab.Screen name="Goals" component={GoalsScreen} />
    <Tab.Screen name="Portfolio" component={PortfolioScreen} />
    <Tab.Screen name="Chat" component={AIChatScreen} />
  </Tab.Navigator>
);

export default function RootNavigator() {
  const { user, loadFromStorage } = useAuthStore();
  console.log('RootNavigator: current user state', user ? user.email : 'null');

  useEffect(() => {
    console.log('RootNavigator: component mounted, calling loadFromStorage');
    loadFromStorage();
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {user ? (
          <Stack.Screen name="App" component={AppNavigator} />
        ) : (
          <Stack.Screen name="Onboarding" component={OnboardingNavigator} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
