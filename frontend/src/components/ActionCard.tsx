// frontend/src/components/ActionCard.tsx
import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { WealthAction } from '../types/api';

interface Props {
  action: WealthAction;
  onPress: () => void;
}

export const ActionCard: React.FC<Props> = ({ action, onPress }) => {
  const getAccentColor = () => {
    if (action.urgency === 'immediate') return '#E63946'; // Deep Crimson (Error)
    if (action.urgency === 'this_week') return '#FF9B3D'; // Ember Amber (Warning)
    return '#00E5C0'; // Electric Teal (Primary)
  };

  return (
    <TouchableOpacity 
      onPress={onPress} 
      activeOpacity={0.7}
      className="bg-surface rounded-xl border border-borderWhite my-2 flex-row"
      style={{ overflow: 'hidden' }}
    >
      <View style={{ width: 4, backgroundColor: getAccentColor() }} />
      <View className="p-4 flex-1">
        <Text className="text-textPrimary font-bold text-base leading-tight">{action.title}</Text>
        <Text className="text-textPrimary opacity-60 text-sm mt-1.5 leading-snug">{action.description}</Text>
        
        <View className="flex-row items-center mt-3 justify-between">
          <View className="bg-primary/50 px-2 py-1 rounded border border-borderWhite">
            <Text className="text-accent text-[10px] font-bold uppercase tracking-[1]">
              {action.impact_level} Impact
            </Text>
          </View>
          {action.expected_impact_description && (
            <Text className="text-textPrimary opacity-40 text-[10px] italic">
              {action.expected_impact_description}
            </Text>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
};
