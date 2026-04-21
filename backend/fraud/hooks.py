# backend/fraud/hooks.py
import logging
from typing import Literal, List, Optional
from pydantic import BaseModel
from datetime import datetime

logger = logging.getLogger(__name__)

class FraudCheckResult(BaseModel):
    fraud_check: Literal["STUB", "ACTIVE"]
    status: Literal["pass", "warn", "block"]
    risk_score: int # 0-100
    risk_level: Literal["low", "medium", "high"]
    triggered_signals: List[str]
    message: str

def _create_stub_result(message: str) -> FraudCheckResult:
    return FraudCheckResult(
        fraud_check="STUB",
        status="pass",
        risk_score=0,
        risk_level="low",
        triggered_signals=[],
        message=message
    )

# FRAUD_HOOK: check_device_trust
def check_device_trust(user_id: int, device_fingerprint: str) -> FraudCheckResult:
    logger.info(f"FRAUD_HOOK: check_device_trust for user {user_id}")
    return _create_stub_result("Device trust check passed (STUB)")

# FRAUD_HOOK: check_session_speed
def check_session_speed(user_id: int, action_timestamp: datetime, login_timestamp: datetime) -> FraudCheckResult:
    logger.info(f"FRAUD_HOOK: check_session_speed for user {user_id}")
    return _create_stub_result("Session speed check passed (STUB)")

# FRAUD_HOOK: check_amount_anomaly
def check_amount_anomaly(user_id: int, amount: float, category: str) -> FraudCheckResult:
    logger.info(f"FRAUD_HOOK: check_amount_anomaly for user {user_id}")
    return _create_stub_result("Amount anomaly check passed (STUB)")

# FRAUD_HOOK: check_otp_pattern
def check_otp_pattern(user_id: int, otp_attempt_count: int) -> FraudCheckResult:
    logger.info(f"FRAUD_HOOK: check_otp_pattern for user {user_id}")
    return _create_stub_result("OTP pattern check passed (STUB)")

# FRAUD_HOOK: check_first_time_action
def check_first_time_action(user_id: int, action_type: str, entity_id: Optional[int]) -> FraudCheckResult:
    logger.info(f"FRAUD_HOOK: check_first_time_action for user {user_id}")
    return _create_stub_result("First time action check passed (STUB)")

# FRAUD_HOOK: check_behaviour_consistency
def check_behaviour_consistency(user_id: int, action_sequence: List[str]) -> FraudCheckResult:
    logger.info(f"FRAUD_HOOK: check_behaviour_consistency for user {user_id}")
    return _create_stub_result("Behaviour consistency check passed (STUB)")

# FRAUD_HOOK: main entry point
def run_full_fraud_check(user_id: int, action_context: dict) -> FraudCheckResult:
    logger.info(f"FRAUD_HOOK: run_full_fraud_check for user {user_id}")
    # This would call all individual checks and aggregate results
    return _create_stub_result("Full fraud check passed (STUB)")
