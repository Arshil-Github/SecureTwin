# backend/tests/test_integration.py
import pytest
import httpx
from datetime import datetime

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_priya_journey():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Login (Priya is already seeded)
        login_res = await client.post("/auth/login", json={"email": "priya@example.com", "password": "Demo@1234"})
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        user_id = login_res.json()["user"]["id"]

        # 2. Get Wealth Snapshot
        snapshot_res = await client.get("/wealth/snapshot", headers=headers)
        assert snapshot_res.status_code == 200
        assert snapshot_res.json()["net_worth"] > 0
        
        # 3. Get Behaviour Stress Score
        stress_res = await client.get("/transactions/behaviour/stress-score", headers=headers)
        assert stress_res.status_code == 200
        assert 0 <= stress_res.json()["score"] <= 100

        # 4. Get Insights Actions
        actions_res = await client.get("/insights/actions", headers=headers)
        assert actions_res.status_code == 200
        assert len(actions_res.json()) >= 0

        # 5. Get Upcoming Calendar
        cal_res = await client.get("/calendar/upcoming", headers=headers)
        assert cal_res.status_code == 200
        
        # 6. AI Chat Message
        chat_res = await client.post("/ai/message", json={
            "user_message": "How is my net worth doing?",
            "conversation_history": [],
            "user_id": user_id
        }, headers=headers)
        assert chat_res.status_code == 200
        assert "assistant_message" in chat_res.json()

        print("Integration test passed for Priya")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_priya_journey())
