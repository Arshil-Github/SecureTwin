# Fraud Layer Integration Guide

This document outlines the requirements for implementing the active fraud detection layer for SecureWealth Twin.

## Overview
Currently, the system uses stubs (marked with `# FRAUD_HOOK`) that return a generic "pass" result. The goal is to replace these with real-time analysis.

## FraudCheckResult Schema
```python
class FraudCheckResult(BaseModel):
    fraud_check: Literal["STUB", "ACTIVE"]
    status: Literal["pass", "warn", "block"]
    risk_score: int # 0-100
    risk_level: Literal["low", "medium", "high"]
    triggered_signals: List[str]
    message: str
```
- **low**: Proceed silently.
- **medium**: Prompt user for confirmation (handled by `FraudWarningModal` in frontend).
- **high**: Block the action immediately.

## Hook Inventory

1. **check_device_trust(user_id, device_fingerprint)**
   - Context: Auth register/login.
   - Behavior: Verify if device is in user's trusted list.

2. **check_session_speed(user_id, action_timestamp, login_timestamp)**
   - Context: High-value actions (transfers, liquidations).
   - Behavior: Detect bot-like speed.

3. **check_amount_anomaly(user_id, amount, category)**
   - Context: Transaction ingestion, manual asset entry.
   - Behavior: Flag if amount > 5x user's historical average for category.

4. **run_full_fraud_check(user_id, action_context)**
   - Main entry point for all mutating operations.
   - Should orchestrate all relevant sub-checks.

## Frontend Integration
The frontend uses `FraudWarningModal.tsx`. It reacts to the `risk_level`:
- `low`: Auto-confirms.
- `medium`: Shows "Are you sure?" modal.
- `high`: Shows "Action Blocked" modal with contact support link.

## Redis Usage
Use the following key patterns for state:
- `session:{user_id}:login_time`
- `device:{user_id}:fingerprints` (set)
- `action_history:{user_id}` (sorted set)
