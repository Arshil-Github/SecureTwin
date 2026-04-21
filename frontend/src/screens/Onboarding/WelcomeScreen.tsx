// frontend/src/screens/Onboarding/WelcomeScreen.tsx
import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';

export default function WelcomeScreen({ navigation }: any) {
  const insets = useSafeAreaInsets();

  return (
    <View className="flex-1 bg-primary px-8" style={{ paddingTop: insets.top, paddingBottom: insets.bottom }}>
      <View className="flex-1 justify-center">
        <View className="items-center mb-12">
          <View className="w-20 h-20 bg-accent/10 rounded-3xl border border-accent/20 items-center justify-center mb-8">
            <MaterialIcons name="auto-awesome" size={40} color="#00E5C0" />
          </View>
          <Text className="text-textPrimary text-4xl font-bold tracking-[-1] text-center uppercase">SECUREWEALTH</Text>
          <Text className="text-accent text-sm tracking-[3] font-bold mt-2 uppercase">Your Twin Awaits</Text>
        </View>

        <View className="bg-surface border border-borderWhite p-8 rounded-[32px] mb-12">
          <Text className="text-textPrimary text-2xl font-bold leading-tight mb-4">Contextual Financial Intelligence.</Text>
          <Text className="text-textPrimary opacity-60 text-base leading-relaxed">
            Experience a premium, AI-native financial companion designed to decode your future.
          </Text>
        </View>
      </View>

      <TouchableOpacity 
        activeOpacity={0.8}
        className="bg-accent py-5 rounded-full items-center mb-6 shadow-lg shadow-accent/40"
        onPress={() => navigation.navigate('KYC')}
      >
        <Text className="text-primary font-bold text-base uppercase tracking-widest">Begin Sync</Text>
      </TouchableOpacity>
      
      <Text className="text-textPrimary opacity-30 text-[10px] uppercase text-center tracking-widest mb-4">
        Protected by SecureWealth Encryption
      </Text>
    </View>
  );
}
