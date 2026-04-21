// frontend/src/components/RiskBadge.tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { colors } from '../theme/colors';

interface Props {
  level: 'low' | 'medium' | 'high';
}

export const RiskBadge: React.FC<Props> = ({ level }) => (
  <View style={[styles.badge, styles[level]]}>
    <Text style={styles.text}>{level.toUpperCase()}</Text>
  </View>
);

const styles = StyleSheet.create({
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 12,
  },
  text: {
    color: '#fff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  low: { backgroundColor: colors.status.success },
  medium: { backgroundColor: colors.status.warning },
  high: { backgroundColor: colors.status.danger },
});
