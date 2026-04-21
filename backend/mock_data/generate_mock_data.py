# backend/mock_data/generate_mock_data.py
import json
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
import bcrypt
import os

fake = Faker('en_IN')

# Personas
PERSONAS = {
    "priya": {
        "id": 1,
        "email": "priya@example.com",
        "full_name": "Priya Sharma",
        "age": 28,
        "income": 85000,
        "risk": "moderate",
        "style": "High food, subscriptions, travel",
        "stress": "month-end spike"
    },
    "ramesh": {
        "id": 2,
        "email": "ramesh@example.com",
        "full_name": "Ramesh Kulkarni",
        "age": 45,
        "income": 220000,
        "risk": "conservative",
        "style": "High utilities, salaries, stable",
        "stress": "income irregularity"
    },
    "ananya": {
        "id": 3,
        "email": "ananya@example.com",
        "full_name": "Ananya Iyer",
        "age": 23,
        "income": 42000,
        "risk": "aggressive",
        "style": "High entertainment, dining, impulsive",
        "stress": "lives paycheck to paycheck"
    }
}

MERCHANTS = {
    "FOOD": ["Swiggy", "Zomato", "BigBasket", "FreshToHome", "McDonalds", "Starbucks"],
    "SHOPPING": ["Amazon", "Flipkart", "Myntra", "Ajio", "Decathlon"],
    "TRANSPORT": ["Ola", "Uber", "IndiGo", "IRCTC", "Petrol Pump"],
    "UTILITIES": ["BESCOM", "Airtel", "Jio", "Netflix", "Spotify", "Cult.fit"],
    "EMI": ["HDFC Home Loan", "ICICI Car Loan", "Bajaj Finance"],
    "INVESTMENT": ["Zerodha", "Groww", "HDFC Mutual Fund", "SBI Mutual Fund"],
}

DIRTY_PREFIXES = ["SWGY*", "swiggy@icici", "SWG FOOD", "ZOMTO ORDER", "AMZN MKTP", "FLPKRT PYMNT"]

def generate_transactions(persona_name):
    p = PERSONAS[persona_name]
    transactions = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    current_balance = p["income"] * 2 # Initial balance
    
    for i in range(180):
        current_date = start_date + timedelta(days=i)
        
        # Salary Credit
        if current_date.day == 1:
            income = p["income"]
            if persona_name == "ramesh":
                income = int(income * random.uniform(0.7, 1.3))
            
            transactions.append({
                "txn_id": str(uuid.uuid4()),
                "amount": income,
                "type": "credit",
                "merchant_raw": "SALARY CREDIT",
                "merchant_normalized": "Salary",
                "category": "INCOME",
                "source": "bank",
                "timestamp": current_date.replace(hour=10, minute=0).isoformat(),
                "balance_after": current_balance + income,
                "description": "Monthly Salary"
            })
            current_balance += income

        # Rent/EMI Debit
        if current_date.day == 5:
            rent = p["income"] * 0.3
            transactions.append({
                "txn_id": str(uuid.uuid4()),
                "amount": rent,
                "type": "debit",
                "merchant_raw": "RENT PAYMENT",
                "merchant_normalized": "Housing",
                "category": "OTHER",
                "source": "bank",
                "timestamp": current_date.replace(hour=9, minute=0).isoformat(),
                "balance_after": current_balance - rent,
                "description": "Monthly Rent"
            })
            current_balance -= rent

        # Daily Transactions
        num_txns = random.randint(1, 4)
        
        # Stress signal: Spikes in last week
        if current_date.day > 23 and persona_name in ["priya", "ananya"]:
            num_txns += random.randint(2, 5)

        for _ in range(num_txns):
            cat = random.choice(list(MERCHANTS.keys()))
            merchant = random.choice(MERCHANTS[cat])
            amount = random.uniform(100, 2000)
            
            if cat == "FOOD" and persona_name == "priya": amount *= 1.5
            if cat == "ENTERTAINMENT" and persona_name == "ananya": amount *= 2.0
            
            is_dirty = random.random() < 0.2
            merchant_raw = merchant
            if is_dirty:
                merchant_raw = random.choice(DIRTY_PREFIXES) + " " + str(random.randint(1000, 9999))

            timestamp = current_date.replace(hour=random.randint(8, 22), minute=random.randint(0, 59))
            
            txn = {
                "txn_id": str(uuid.uuid4()),
                "amount": round(amount, 2),
                "type": "debit",
                "merchant_raw": merchant_raw,
                "merchant_normalized": merchant,
                "category": cat,
                "source": random.choice(["UPI", "bank"]),
                "timestamp": timestamp.isoformat(),
                "balance_after": round(current_balance - amount, 2),
                "description": f"Purchase at {merchant}",
                "is_recurring": random.random() < 0.1
            }
            transactions.append(txn)
            current_balance -= amount

            # Deduplication test case (20% of the time for UPI)
            if txn["source"] == "UPI" and random.random() < 0.1:
                dup_txn = txn.copy()
                dup_txn["txn_id"] = str(uuid.uuid4())
                dup_txn["source"] = "bank"
                dup_txn["timestamp"] = (timestamp + timedelta(minutes=random.randint(-2, 2))).isoformat()
                dup_txn["description"] = f"UPI/BANK DUP: {merchant}"
                transactions.append(dup_txn)

    return {
        "metadata": {
            "persona_id": p["id"],
            "date_range": [start_date.isoformat(), end_date.isoformat()],
            "total_transactions": len(transactions)
        },
        "transactions": transactions
    }

def generate_investments(persona_name):
    if persona_name == "priya":
        return [
            {
                "account_type": "mutual_fund",
                "scheme_name": "Axis Bluechip Fund",
                "invested_amount": 40000,
                "current_value": 45200,
                "sip_amount": 5000,
                "returns_xirr": 14.2,
                "start_date": (datetime.now() - timedelta(days=240)).isoformat()
            },
            {
                "account_type": "mutual_fund",
                "scheme_name": "Mirae Asset Large Cap",
                "invested_amount": 40000,
                "current_value": 44800,
                "sip_amount": 5000,
                "returns_xirr": 12.8,
                "start_date": (datetime.now() - timedelta(days=240)).isoformat()
            },
            {
                "account_type": "fd",
                "scheme_name": "HDFC Fixed Deposit",
                "invested_amount": 50000,
                "current_value": 53550,
                "interest_rate": 7.1,
                "maturity_date": (datetime.now() + timedelta(days=180)).isoformat()
            }
        ]
    elif persona_name == "ramesh":
        return [
            {"account_type": "fd", "scheme_name": "SBI FD 1", "invested_amount": 500000, "current_value": 535000, "interest_rate": 7.0},
            {"account_type": "fd", "scheme_name": "HDFC FD 2", "invested_amount": 200000, "current_value": 210000, "interest_rate": 7.2},
            {"account_type": "ppf", "scheme_name": "PPF", "invested_amount": 1200000, "current_value": 1800000, "interest_rate": 7.1},
            {"account_type": "rd", "scheme_name": "Monthly RD", "invested_amount": 90000, "current_value": 94000, "sip_amount": 5000}
        ]
    else: # ananya
        return []

def generate_assets(persona_name):
    if persona_name == "priya":
        return [
            {"asset_type": "gold", "name": "Gold Jewelry (10g)", "purchase_value": 50000, "current_value": 62000},
            {"asset_type": "vehicle", "name": "Honda Activa", "purchase_value": 75000, "current_value": 45000}
        ]
    elif persona_name == "ramesh":
        return [
            {"asset_type": "property", "name": "Commercial Shop Pune", "purchase_value": 5000000, "current_value": 6500000},
            {"asset_type": "gold", "name": "Gold Bars (50g)", "purchase_value": 250000, "current_value": 310000},
            {"asset_type": "vehicle", "name": "Toyota Innova", "purchase_value": 2500000, "current_value": 1800000}
        ]
    else:
        return []

def main():
    os.makedirs('backend/mock_data', exist_ok=True)
    
    users = []
    for name, p in PERSONAS.items():
        # User
        password = "Demo@1234"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        user = {
            "id": p["id"],
            "email": p["email"],
            "hashed_password": hashed,
            "full_name": p["full_name"],
            "age": p["age"],
            "monthly_income": p["income"],
            "risk_appetite": p["risk"],
            "is_kyc_verified": True,
            "trusted_devices": [f"device_fingerprint_{p['id']}"]
        }
        users.append(user)

        # Transactions
        txns_data = generate_transactions(name)
        with open(f'backend/mock_data/transactions_{name}.json', 'w') as f:
            json.dump(txns_data, f, indent=2)

        # Investments
        investments = generate_investments(name)
        with open(f'backend/mock_data/investments_{name}.json', 'w') as f:
            json.dump({"investments": investments}, f, indent=2)

        # Assets
        assets = generate_assets(name)
        with open(f'backend/mock_data/assets_{name}.json', 'w') as f:
            json.dump({"assets": assets}, f, indent=2)

    with open('backend/mock_data/users.json', 'w') as f:
        json.dump({"users": users}, f, indent=2)

    print("Mock data generated successfully.")

if __name__ == "__main__":
    main()
