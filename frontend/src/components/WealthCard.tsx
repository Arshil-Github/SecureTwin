// frontend/src/components/WealthCard.tsx
import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

interface Props {
  title: string;
  value: string;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  onPress?: () => void;
}

export const WealthCard: React.FC<Props> = ({ title, value, subtitle, trend, trendValue, onPress }) => (
  <TouchableOpacity 
    onPress={onPress} 
    disabled={!onPress} 
    activeOpacity={0.8}
    className="bg-surface p-6 rounded-2xl my-3 border border-borderWhite"
    style={{ backdropFilter: 'blur(10px)' } as any} // backdrop-blur for web, ignored by mobile usually but kept for 'glass' feel if supported by engine
  >
    <Text className="text-textPrimary opacity-60 text-xs uppercase tracking-[2] font-medium mb-1">{title}</Text>
    <Text className="text-textPrimary text-4xl font-bold tracking-[-0.5]">{value}</Text>
    {trend && (
      <View className="flex-row items-center mt-3">
        <View 
          className={`w-2 h-2 rounded-full mr-2 ${trend === 'up' ? 'bg-accent' : 'bg-danger'}`} 
          style={{ shadowColor: trend === 'up' ? '#00E5C0' : '#E63946', shadowRadius: 4, shadowOpacity: 0.5, elevation: 4 }}
        />
        <Text className={`text-sm font-bold ${trend === 'up' ? 'text-accent' : 'text-danger'}`}>
          {trend === 'up' ? '+' : '-'} {trendValue}
        </Text>
        {subtitle && <Text className="text-textPrimary opacity-40 text-xs ml-2">{subtitle}</Text>}
      </View>
    )}
  </TouchableOpacity>
);
