# backend/utils/xirr.py
from datetime import date
from scipy.optimize import newton

def xirr(cashflows: list[tuple[date, float]]) -> float:
    """
    Calculate XIRR using Newton-Raphson.
    cashflows: list of (date, amount)
    """
    if not cashflows or len(cashflows) < 2:
        return None

    def xnpv(rate, cashflows):
        t0 = cashflows[0][0]
        return sum([cf / (1 + rate)**((d - t0).days / 365.0) for d, cf in cashflows])

    try:
        return newton(lambda r: xnpv(r, cashflows), 0.1)
    except (RuntimeError, OverflowError, ZeroDivisionError):
        return None

if __name__ == "__main__":
    # Test Cases
    from datetime import date, timedelta
    
    # 1. Simple SIP
    today = date.today()
    cf_sip = [
        (today - timedelta(days=365), -10000),
        (today - timedelta(days=180), -10000),
        (today, 22000)
    ]
    print(f"SIP XIRR: {xirr(cf_sip):.2%}")
    
    # 2. FD
    cf_fd = [
        (today - timedelta(days=365), -100000),
        (today, 107100)
    ]
    print(f"FD XIRR: {xirr(cf_fd):.2%}")
    
    # 3. Edge Case
    print(f"Single CF: {xirr([(today, -100)])}")
