// frontend/src/screens/Dashboard/DashboardScreen.tsx
import React, { useEffect } from 'react';
import { ScrollView, View, Text, RefreshControl, TouchableOpacity } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Svg, Path, Defs, LinearGradient, Stop } from 'react-native-svg';
import { Ionicons, MaterialIcons } from '@expo/vector-icons';
import { useWealthStore } from '../../store/useWealthStore';
import { useGoalStore } from '../../store/useGoalStore';
import { ActionCard } from '../../components/ActionCard';
import { SkeletonCard } from '../../components/SkeletonLoader';

export default function DashboardScreen() {
  const insets = useSafeAreaInsets();
  const { snapshot, actions, isLoading, fetchSnapshot, fetchActions } = useWealthStore();
  const { goals, fetchGoals } = useGoalStore();

  useEffect(() => {
    onRefresh();
  }, []);

  const onRefresh = () => {
    fetchSnapshot();
    fetchActions();
    fetchGoals();
  };

  const PulseChart = () => (
    <View className="h-24 w-full mt-4">
      <Svg width="100%" height="100%" viewBox="0 0 100 40" preserveAspectRatio="none">
        <Defs>
          <LinearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <Stop offset="0%" stopColor="#00e5c0" stopOpacity="0.4" />
            <Stop offset="50%" stopColor="#00e5c0" stopOpacity="1" />
            <Stop offset="100%" stopColor="#00e5c0" stopOpacity="0.6" />
          </LinearGradient>
          <LinearGradient id="fillGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <Stop offset="0%" stopColor="#00e5c0" stopOpacity="0.15" />
            <Stop offset="100%" stopColor="#00e5c0" stopOpacity="0" />
          </LinearGradient>
        </Defs>
        <Path 
          d="M0,40 L0,30 C20,35 30,15 50,20 C70,25 80,5 100,10 L100,40 Z" 
          fill="url(#fillGrad)" 
        />
        <Path 
          d="M0,30 C20,35 30,15 50,20 C70,25 80,5 100,10" 
          fill="none" 
          stroke="url(#lineGrad)" 
          strokeWidth="2" 
        />
      </Svg>
    </View>
  );

  if (isLoading && !snapshot) {
    return (
      <View className="flex-1 bg-primary px-6" style={{ paddingTop: insets.top + 20 }}>
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-primary">
      {/* Header */}
      <View 
        className="px-6 py-4 flex-row justify-between items-center border-b border-borderWhite bg-primary/80"
        style={{ paddingTop: insets.top }}
      >
        <TouchableOpacity>
          <MaterialIcons name="account-balance-wallet" size={24} color="#00E5C0" />
        </TouchableOpacity>
        <Text className="font-bold text-lg tracking-tighter text-textPrimary uppercase">SECUREWEALTH</Text>
        <TouchableOpacity>
          <Ionicons name="notifications-outline" size={24} color="#00E5C0" />
        </TouchableOpacity>
      </View>

      <ScrollView 
        className="flex-1"
        contentContainerClassName="px-6 pt-8 pb-12"
        refreshControl={<RefreshControl refreshing={isLoading} onRefresh={onRefresh} tintColor="#00E5C0" />}
      >
        {/* Contextual Greeting */}
        <View className="mb-8">
          <Text className="text-textPrimary opacity-50 uppercase tracking-[2] text-[10px] font-bold mb-1">Good Morning</Text>
          <Text className="text-textPrimary text-2xl font-bold leading-tight">
            Your SIP debits tomorrow. Balance is comfortable.
          </Text>
        </View>

        {/* Net Worth Hero */}
        <View className="bg-surface rounded-3xl p-6 border border-borderWhite relative overflow-hidden mb-8">
          <View className="flex-col">
            <Text className="text-textPrimary opacity-60 text-[10px] uppercase tracking-widest font-bold">Total Net Worth</Text>
            <View className="flex-row items-baseline mt-1">
              <Text className="text-textPrimary text-4xl font-bold">₹{snapshot?.net_worth.toLocaleString() || '0'}</Text>
              <View className="ml-2 bg-accent/10 px-2 py-1 rounded-full">
                <Text className="text-accent text-[10px] font-bold">+2.4%</Text>
              </View>
            </View>
          </View>
          <PulseChart />
        </View>

        {/* Status Cards Bento */}
        <View className="flex-row gap-4 mb-8">
          <View className="flex-1 bg-surface rounded-2xl p-5 border border-borderWhite">
            <View className="flex-row items-center mb-4">
              <Ionicons name="shield-checkmark-outline" size={18} color="#00E5C0" />
              <Text className="ml-2 text-textPrimary opacity-60 text-[10px] uppercase font-bold tracking-[1]">Health</Text>
            </View>
            <View className="flex-row items-baseline mb-2">
              <Text className="text-textPrimary text-3xl font-bold">{snapshot?.portfolio_health_score || 0}</Text>
              <Text className="text-textPrimary opacity-40 text-xs font-bold ml-1">/100</Text>
            </View>
            <View className="h-1 bg-white/5 rounded-full overflow-hidden">
              <View className="h-full bg-accent rounded-full" style={{ width: `${snapshot?.portfolio_health_score || 0}%` }} />
            </View>
          </View>

          <View className="flex-1 bg-surface rounded-2xl p-5 border border-borderWhite">
            <View className="flex-row items-center mb-4">
              <Ionicons name="wallet-outline" size={18} color="#FF9B3D" />
              <Text className="ml-2 text-textPrimary opacity-60 text-[10px] uppercase font-bold tracking-[1]">Savings</Text>
            </View>
            <View className="flex-row items-baseline mb-2">
              <Text className="text-textPrimary text-3xl font-bold">18</Text>
              <Text className="text-textPrimary opacity-40 text-xs font-bold ml-1">%</Text>
            </View>
            <View className="h-1 bg-white/5 rounded-full overflow-hidden">
              <View className="h-full bg-warning w-[18%] rounded-full" />
            </View>
          </View>
        </View>

        {/* Today's Focus */}
        <View>
          <Text className="text-textPrimary opacity-50 uppercase tracking-[2] text-[10px] font-bold mb-4">Today's Focus</Text>
          {actions.map(action => (
            <ActionCard 
              key={action.action_id} 
              action={action} 
              onPress={() => alert(`Executing: ${action.title}\n\n${action.expected_impact_description}`)} 
            />
          ))}
        </View>
        </ScrollView>
        {/* Goal Progress */}
        <View>
          <Text className="text-textPrimary opacity-50 uppercase tracking-[2] text-[10px] font-bold mb-4">Goal Progress</Text>
          {goals.map(goal => {
            const progress = (goal.health.current_amount / goal.target_amount) * 100;
            return (
              <View key={goal.id} className="bg-surface rounded-2xl p-5 border border-borderWhite mb-4">
                <View className="flex-row justify-between items-center mb-2">
                  <Text className="text-textPrimary text-sm font-bold">{goal.name}</Text>
                  <Text className="text-textPrimary text-sm font-bold">{Math.round(progress)}%</Text>
                </View>
                <View className="h-1 bg-white/5 rounded-full overflow-hidden">
                  <View className="h-full bg-accent rounded-full" style={{ width: `${progress}%` }} />
                </View>
              </View>
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}

