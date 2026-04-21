# backend/utils/merchant_normalizer.py
import re
import difflib
from dataclasses import dataclass
from typing import Optional

@dataclass
class MerchantResult:
    canonical_name: str
    category: str
    sub_category: Optional[str] = None
    confidence: float = 1.0

MERCHANT_MAP = [
    # Patterns for regex matching
    (r"(?i)SWIGGY|SWGY", "Swiggy", "FOOD", "Food Delivery"),
    (r"(?i)ZOMATO|ZOMTO", "Zomato", "FOOD", "Food Delivery"),
    (r"(?i)BIGBASKET|BIG BASKET", "BigBasket", "SHOPPING", "Grocery"),
    (r"(?i)AMAZON|AMZN", "Amazon", "SHOPPING", "E-commerce"),
    (r"(?i)FLIPKART|FLPKRT", "Flipkart", "SHOPPING", "E-commerce"),
    (r"(?i)OLA", "Ola", "TRANSPORT", "Cabs"),
    (r"(?i)UBER", "Uber", "TRANSPORT", "Cabs"),
    (r"(?i)NETFLIX|NFLX", "Netflix", "UTILITIES", "Subscription"),
    (r"(?i)SPOTIFY", "Spotify", "UTILITIES", "Subscription"),
    (r"(?i)AIRTEL", "Airtel", "UTILITIES", "Mobile/Broadband"),
    (r"(?i)JIO", "Jio", "UTILITIES", "Mobile/Broadband"),
    (r"(?i)BESCOM", "BESCOM", "UTILITIES", "Electricity"),
    (r"(?i)MSEB", "MSEB", "UTILITIES", "Electricity"),
    (r"(?i)SALARY|SAL CREDIT", "Salary", "INCOME", "Monthly Salary"),
    (r"(?i)RENT PAYMENT", "Rent", "OTHER", "Housing"),
    (r"(?i)CULT\.FIT|CULTFIT", "Cult.fit", "HEALTH", "Fitness"),
    (r"(?i)STARBUCKS", "Starbucks", "FOOD", "Dining"),
    (r"(?i)MCDONALDS", "McDonalds", "FOOD", "Dining"),
]

# Known canonical names for fuzzy matching
CANONICAL_NAMES = [m[1] for m in MERCHANT_MAP]

_cache = {}

def normalize(raw_string: str) -> MerchantResult:
    raw_string = raw_string.strip()
    if raw_string in _cache:
        return _cache[raw_string]

    # 1. Regex Match
    for pattern, canonical, category, sub_cat in MERCHANT_MAP:
        if re.search(pattern, raw_string):
            res = MerchantResult(canonical, category, sub_cat, 1.0)
            _cache[raw_string] = res
            return res

    # 2. Fuzzy Match
    matches = difflib.get_close_matches(raw_string.upper(), [name.upper() for name in CANONICAL_NAMES], n=1, cutoff=0.8)
    if matches:
        matched_name = matches[0]
        # Find the original canonical name and its data
        for _, canonical, category, sub_cat in MERCHANT_MAP:
            if canonical.upper() == matched_name:
                res = MerchantResult(canonical, category, sub_cat, 0.9)
                _cache[raw_string] = res
                return res

    # 3. Default
    res = MerchantResult(raw_string.title(), "OTHER", None, 0.5)
    _cache[raw_string] = res
    return res

if __name__ == "__main__":
    test_cases = [
        "SWGY*8823", "swiggy@icici", "SWG FOOD", "ZOMTO ORDER",
        "NFLX.COM", "BESCOM BILL", "SAL CREDIT INFOSYS", "CULTFIT GYM"
    ]
    for tc in test_cases:
        print(f"'{tc}' -> {normalize(tc)}")
