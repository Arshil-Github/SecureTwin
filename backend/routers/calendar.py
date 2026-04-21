# backend/routers/calendar.py
from fastapi import APIRouter, Depends
from typing import List
from backend.services.financial_calendar import FinancialCalendar, CalendarEvent, MonthlyCalendar

router = APIRouter()

# Mock Auth
async def get_current_user_id():
    return 1

@router.get("/upcoming", response_model=List[CalendarEvent])
async def get_upcoming(days: int = 30, user_id: int = Depends(get_current_user_id)):
    cal = FinancialCalendar()
    return await cal.get_upcoming_events(user_id, days)

@router.get("/month", response_model=MonthlyCalendar)
async def get_month(month: int, year: int, user_id: int = Depends(get_current_user_id)):
    cal = FinancialCalendar()
    return await cal.get_monthly_calendar(user_id, month, year)
