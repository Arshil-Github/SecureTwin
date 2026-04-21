// frontend/src/components/SkeletonLoader.tsx
import React from 'react';
import { View } from 'react-native';

export const SkeletonCard = () => (
  <View 
    className="bg-surface rounded-2xl my-2 border border-borderWhite"
    style={{ height: 120, opacity: 0.3 }}
  />
);
