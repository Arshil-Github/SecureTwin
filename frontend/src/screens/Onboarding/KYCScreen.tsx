// frontend/src/screens/Onboarding/KYCScreen.tsx
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { useAuthStore } from '../../store/useAuthStore';
import { colors } from '../../theme/colors';

export default function KYCScreen() {
  const { login, isLoading } = useAuthStore();

  const loginAsPriya = async () => {
    console.log('KYCScreen: loginAsPriya clicked');
    try {
      // Use the correct fingerprint matching users.json for Priya
      await login('priya@example.com', 'Demo@1234', 'device_fingerprint_1');
      console.log('KYCScreen: login call finished');
    } catch (err: any) {
      console.error('KYCScreen: login failed', err);
      Alert.alert('Login Failed', err.message || 'Check console for details');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Select Persona for Demo</Text>
      
      <TouchableOpacity 
        style={[styles.button, isLoading ? { opacity: 0.5 } : {}]} 
        onPress={loginAsPriya}
        disabled={!!isLoading}
      >
        <Text style={styles.buttonText}>
          {isLoading ? 'Logging in...' : 'Login as Priya'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    padding: 24,
  },
  title: {
    fontSize: 24,
    color: '#fff',
    fontWeight: 'bold',
    marginBottom: 32,
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#1A2B48',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: colors.accent,
    fontWeight: 'bold',
    fontSize: 18,
  },
});
