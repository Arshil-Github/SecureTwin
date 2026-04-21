// frontend/src/screens/Goals/GoalsScreen.tsx
import React, { useEffect } from 'react';
import { ScrollView, View, Text, TouchableOpacity, RefreshControl } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialIcons } from '@expo/vector-icons';
import { useGoalStore } from '../../store/useGoalStore';

export default function GoalsScreen() {
  const insets = useSafeAreaInsets();
  const { goals, conflicts, isLoading, fetchGoals, fetchConflicts } = useGoalStore();

  useEffect(() => {
    fetchGoals();
    fetchConflicts();
  }, []);

  const ConflictCard = ({ conflict }: { conflict: any }) => (
    <View className="bg-surface rounded-3xl p-6 border border-borderWhite mb-8 relative overflow-hidden">
      <View className="absolute top-0 left-0 right-0 h-[2px] bg-warning/50" />
      <View className="flex-row items-start gap-4">
        <View className="bg-warning/10 p-2 rounded-lg">
          <Ionicons name="warning" size={20} color="#FF9B3D" />
        </View>
        <View className="flex-1">
          <Text className="text-warning text-[10px] uppercase font-bold tracking-[2] mb-1">Conflict Detected</Text>
          <Text className="text-textPrimary text-sm leading-tight mb-3">
            {conflict.message}
          </Text>
          <TouchableOpacity className="flex-row items-center">
            <Text className="text-warning text-[10px] font-bold uppercase tracking-[2] mr-1">Resolve Strategy</Text>
            <Ionicons name="arrow-forward" size={12} color="#FF9B3D" />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );

  const onRefresh = () => {
    fetchGoals();
    fetchConflicts();
  };

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
        <Text className="font-bold text-lg tracking-tighter text-textPrimary uppercase">GOALS</Text>
        <TouchableOpacity>
          <Ionicons name="notifications-outline" size={24} color="#00E5C0" />
        </TouchableOpacity>
      </View>

      <ScrollView 
        className="flex-1" 
        contentContainerClassName="px-6 pt-8 pb-32"
        refreshControl={<RefreshControl refreshing={isLoading} onRefresh={onRefresh} tintColor="#00E5C0" />}
      >
        <View className="mb-8">
          <Text className="text-textPrimary text-4xl font-bold tracking-[-0.5] mb-1">Goals Overview</Text>
          <Text className="text-textPrimary opacity-50 text-sm">Your wealth trajectory and active targets.</Text>
        </View>

        {conflicts && conflicts.length > 0 && conflicts.map((conflict, index) => (
          <ConflictCard key={index} conflict={conflict} />
        ))}

        <View className="gap-6">
          {goals.map(goal => {
            const progress = (goal.health.current_amount / goal.target_amount) * 100;
            const isAtRisk = goal.health.status === 'at_risk' || goal.health.status === 'off_track';
            
            return (
              <TouchableOpacity key={goal.id} className="bg-surface border border-borderWhite p-6 rounded-3xl relative overflow-hidden">
                <View className="flex-row justify-between items-start mb-8">
                  <View className="flex-row items-center gap-4">
                    <View className="w-12 h-12 rounded-full bg-primary border border-borderWhite items-center justify-center">
                      <MaterialIcons 
                        name={goal.name.toLowerCase().includes('home') ? 'home' : 'health-and-safety'} 
                        size={24} 
                        color="#F2EDE4" 
                      />
                    </View>
                    <View>
                      <Text className="text-textPrimary text-xl font-bold leading-none">{goal.name}</Text>
                      <View className="flex-row items-center gap-1 mt-1.5">
                        <View className={`w-1.5 h-1.5 rounded-full ${isAtRisk ? 'bg-danger' : 'bg-accent'}`} />
                        <Text className={`text-[10px] uppercase font-bold tracking-[2] ${isAtRisk ? 'text-danger' : 'text-accent'}`}>
                          {goal.health.status.replace('_', ' ')}
                        </Text>
                      </View>
                    </View>
                  </View>
                  <View className="items-end">
                    <Text className="text-textPrimary text-3xl font-bold">{Math.round(progress)}%</Text>
                    <Text className="text-textPrimary opacity-40 text-[10px] uppercase font-bold tracking-[2] mt-1">Complete</Text>
                  </View>
                </View>

                <View className="space-y-3">
                  <View className="h-2 bg-white/5 rounded-full overflow-hidden">
                    <View 
                      style={{ width: `${progress}%` }} 
                      className={`h-full rounded-full ${isAtRisk ? 'bg-danger' : 'bg-accent'}`} 
                    />
                  </View>
                  <View className="flex-row items-center gap-1.5">
                    <Ionicons 
                      name={isAtRisk ? "trending-down" : "trending-up"} 
                      size={14} 
                      color={isAtRisk ? "#E63946" : "#00E5C0"} 
                    />
                    <Text className="text-textPrimary opacity-40 text-[10px] font-medium">
                      {isAtRisk 
                        ? `Gap indicator: Need ₹${goal.monthly_contribution.toLocaleString()}/mo` 
                        : `Projected completion: ${goal.target_date}`}
                    </Text>
                  </View>
                </View>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}
iew>
                </View>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}
