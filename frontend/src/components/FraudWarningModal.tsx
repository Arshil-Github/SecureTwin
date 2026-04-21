// frontend/src/components/FraudWarningModal.tsx
// FRAUD_HOOK: This modal will be replaced with full fraud UI
import React, { useEffect } from 'react';
import { Modal, View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { FraudCheckResult } from '../types/api';

interface Props {
  visible: boolean;
  result: FraudCheckResult;
  onConfirm: () => void;
  onCancel: () => void;
  onFraudEvent?: (result: FraudCheckResult) => void;
}

export const FraudWarningModal: React.FC<Props> = ({ visible, result, onConfirm, onCancel, onFraudEvent }) => {
  useEffect(() => {
    if (visible && result.risk_level === 'low') {
      onConfirm();
    }
    if (visible && onFraudEvent) {
      onFraudEvent(result);
    }
  }, [visible, result.risk_level]);

  if (result.risk_level === 'low') return null;

  return (
    <Modal visible={visible} transparent animationType="slide">
      <View style={styles.overlay}>
        <View style={styles.content}>
          <Text style={styles.title}>{result.risk_level === 'high' ? "Action Blocked" : "Please Confirm"}</Text>
          <Text style={styles.message}>{result.message || "Security validation required."}</Text>
          
          {result.risk_level === 'medium' ? (
            <>
              {/* FRAUD_HOOK: Add 5-second cooling-off timer here */}
              <TouchableOpacity onPress={onConfirm} style={styles.btnConfirm}>
                <Text style={styles.btnText}>Yes, Authorized</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={onCancel} style={styles.btnCancel}>
                <Text style={styles.cancelText}>Cancel</Text>
              </TouchableOpacity>
            </>
          ) : (
            <>
              {/* FRAUD_HOOK: Add "Call your bank" button here */}
              <TouchableOpacity onPress={onCancel} style={styles.btnConfirm}>
                <Text style={styles.btnText}>OK, I understand</Text>
              </TouchableOpacity>
            </>
          )}
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.8)',
    justifyContent: 'center',
    padding: 24,
  },
  content: {
    backgroundColor: '#fff',
    padding: 24,
    borderRadius: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#0A1628',
  },
  message: {
    fontSize: 16,
    marginBottom: 24,
    color: '#444',
  },
  btnConfirm: {
    backgroundColor: '#0A1628',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 12,
  },
  btnText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  btnCancel: {
    alignItems: 'center',
    padding: 8,
  },
  cancelText: {
    color: '#666',
  },
});
