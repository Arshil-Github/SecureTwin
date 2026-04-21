# backend/mock_data/seed_db.py
import asyncio
from sqlalchemy import select
from backend.database import init_db, AsyncSessionLocal
from backend.models.user import User
from backend.models.transaction import Transaction
from backend.models.investment import Investment
from backend.models.asset import Asset
from backend.models.goal import Goal
from backend.mock_data import loader
from datetime import datetime

async def seed_data():
    init_db()
    async with AsyncSessionLocal() as session:
        users = loader.load_all_users()
        for user_data in users:
            # Check if user exists
            result = await session.execute(select(User).where(User.email == user_data['email']))
            user = result.scalars().first()
            if not user:
                user = User(
                    id=user_data['id'],
                    email=user_data['email'],
                    hashed_password=user_data['hashed_password'],
                    full_name=user_data['full_name'],
                    age=user_data['age'],
                    monthly_income=user_data['monthly_income'],
                    risk_appetite=user_data['risk_appetite'],
                    is_kyc_verified=user_data['is_kyc_verified'],
                    trusted_devices=user_data['trusted_devices']
                )
                session.add(user)
                await session.flush()
            
            persona_name = user.full_name.split()[0].lower()
            
            # Seed Goals
            goals_mock = {
                "priya": [
                    {"name": "Home Downpayment", "target": 5000000, "current": 1050000, "date": "2027-12-31", "monthly": 5000},
                    {"name": "Emergency Fund", "target": 300000, "current": 180000, "date": "2025-12-31", "monthly": 15000}
                ],
                "ramesh": [
                    {"name": "Daughter Education", "target": 10000000, "current": 3500000, "date": "2030-05-30", "monthly": 20000},
                    {"name": "Retirement", "target": 50000000, "current": 25000000, "date": "2040-01-01", "monthly": 50000}
                ],
                "ananya": [
                    {"name": "Europe Trip", "target": 400000, "current": 100000, "date": "2026-06-01", "monthly": 8000},
                    {"name": "Emergency Fund", "target": 150000, "current": 20000, "date": "2025-06-01", "monthly": 10000}
                ]
            }

            if persona_name in goals_mock:
                for goal_data in goals_mock[persona_name]:
                    result = await session.execute(select(Goal).where(
                        Goal.user_id == user.id,
                        Goal.name == goal_data['name']
                    ))
                    if not result.scalars().first():
                        g = Goal(
                            user_id=user.id,
                            name=goal_data['name'],
                            target_amount=goal_data['target'],
                            current_amount=goal_data['current'],
                            target_date=datetime.fromisoformat(goal_data['date']),
                            monthly_contribution=goal_data['monthly']
                        )
                        session.add(g)

            # Seed transactions
            txns = loader.load_transactions(persona_name)
            for txn_data in txns:
                result = await session.execute(select(Transaction).where(Transaction.txn_id == txn_data['txn_id']))
                if not result.scalars().first():
                    txn = Transaction(
                        user_id=user.id,
                        txn_id=txn_data['txn_id'],
                        amount=txn_data['amount'],
                        type=txn_data['type'],
                        merchant_raw=txn_data['merchant_raw'],
                        merchant_normalized=txn_data['merchant_normalized'],
                        category=txn_data['category'],
                        source=txn_data['source'],
                        timestamp=datetime.fromisoformat(txn_data['timestamp']),
                        balance_after=txn_data.get('balance_after'),
                        description=txn_data.get('description'),
                        is_recurring=txn_data.get('is_recurring', False)
                    )
                    session.add(txn)

            # Seed investments
            investments = loader.load_investments(persona_name)
            for inv_data in investments:
                # Upsert based on scheme_name for now
                result = await session.execute(select(Investment).where(
                    Investment.user_id == user.id, 
                    Investment.scheme_name == inv_data['scheme_name']
                ))
                if not result.scalars().first():
                    inv = Investment(
                        user_id=user.id,
                        account_type=inv_data['account_type'],
                        scheme_name=inv_data['scheme_name'],
                        invested_amount=inv_data['invested_amount'],
                        current_value=inv_data['current_value'],
                        sip_amount=inv_data.get('sip_amount'),
                        returns_xirr=inv_data.get('returns_xirr'),
                        interest_rate=inv_data.get('interest_rate'),
                        start_date=datetime.fromisoformat(inv_data['start_date']) if 'start_date' in inv_data else None,
                        maturity_date=datetime.fromisoformat(inv_data['maturity_date']) if 'maturity_date' in inv_data else None
                    )
                    session.add(inv)

            # Seed assets
            assets = loader.load_assets(persona_name)
            for asset_data in assets:
                result = await session.execute(select(Asset).where(
                    Asset.user_id == user.id,
                    Asset.name == asset_data['name']
                ))
                if not result.scalars().first():
                    asset = Asset(
                        user_id=user.id,
                        asset_type=asset_data['asset_type'],
                        name=asset_data['name'],
                        purchase_value=asset_data['purchase_value'],
                        current_value=asset_data['current_value']
                    )
                    session.add(asset)

        await session.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_data())

