# backend/services/financial_calendar.py
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel
from sqlalchemy import select
from backend.database import AsyncSessionLocal
from backend.models.investment import Investment
from backend.models.transaction import Transaction

class CalendarEvent(BaseModel):
    event_id: str
    event_type: str # sip_debit, fd_maturity, rd_installment, emi_due, salary_expected
    event_date: date
    title: str
    amount: float
    account_or_goal: str
    is_critical: bool
    balance_warning: Optional[str] = None
    action_suggestion: Optional[str] = None

class MonthlyCalendar(BaseModel):
    month: int
    year: int
    events_by_day: Dict[int, List[CalendarEvent]]
    total_outflows: float
    total_expected_inflows: float
    net_cash_flow_projected: float

class FinancialCalendar:
    
    async def get_upcoming_events(self, user_id: int, days_ahead: int = 30) -> List[CalendarEvent]:
        events = []
        today = date.today()
        end_date = today + timedelta(days=days_ahead)
        
        async with AsyncSessionLocal() as session:
            # 1. SIP Debits & FD Maturities
            res_inv = await session.execute(select(Investment).where(Investment.user_id == user_id))
            investments = res_inv.scalars().all()
            
            for inv in investments:
                if inv.sip_date and inv.sip_amount:
                    # Simplified: next occurrence this month or next
                    event_date = date(today.year, today.month, inv.sip_date)
                    if event_date < today:
                        if today.month == 12:
                            event_date = date(today.year + 1, 1, inv.sip_date)
                        else:
                            event_date = date(today.year, today.month + 1, inv.sip_date)
                    
                    if today <= event_date <= end_date:
                        events.append(CalendarEvent(
                            event_id=f"sip_{inv.id}",
                            event_type="sip_debit",
                            event_date=event_date,
                            title=f"SIP: {inv.scheme_name}",
                            amount=inv.sip_amount,
                            account_or_goal=inv.scheme_name,
                            is_critical=False
                        ))
                
                if inv.maturity_date and today <= inv.maturity_date.date() <= end_date:
                    events.append(CalendarEvent(
                        event_id=f"mat_{inv.id}",
                        event_type="fd_maturity",
                        event_date=inv.maturity_date.date(),
                        title=f"FD Maturity: {inv.scheme_name}",
                        amount=inv.current_value or inv.invested_amount,
                        account_or_goal=inv.scheme_name,
                        is_critical=False,
                        action_suggestion="Plan your reinvestment strategy"
                    ))
            
            # 2. Salary Expected
            res_salary = await session.execute(
                select(Transaction)
                .where(Transaction.user_id == user_id, Transaction.category == "INCOME")
                .order_by(Transaction.timestamp.desc())
                .limit(1)
            )
            last_salary = res_salary.scalars().first()
            if last_salary:
                # Predict next salary date (1st of next month usually)
                next_salary_date = date(today.year, today.month, 1)
                if next_salary_date <= today:
                    if today.month == 12:
                        next_salary_date = date(today.year + 1, 1, 1)
                    else:
                        next_salary_date = date(today.year, today.month + 1, 1)
                
                if today <= next_salary_date <= end_date:
                    events.append(CalendarEvent(
                        event_id="salary_next",
                        event_type="salary_expected",
                        event_date=next_salary_date,
                        title="Expected Salary",
                        amount=last_salary.amount,
                        account_or_goal="Salary Account",
                        is_critical=False
                    ))
                    
        return sorted(events, key=lambda x: x.event_date)

    async def get_monthly_calendar(self, user_id: int, month: int, year: int) -> MonthlyCalendar:
        events = await self.get_upcoming_events(user_id, 60) # Get enough to cover month
        month_events = [e for e in events if e.event_date.month == month and e.event_date.year == year]
        
        events_by_day = {}
        outflows = 0
        inflows = 0
        for e in month_events:
            events_by_day.setdefault(e.event_date.day, []).append(e)
            if e.event_type == 'salary_expected' or e.event_type == 'fd_maturity':
                inflows += e.amount
            else:
                outflows += e.amount
                
        return MonthlyCalendar(
            month=month,
            year=year,
            events_by_day=events_by_day,
            total_outflows=outflows,
            total_expected_inflows=inflows,
            net_cash_flow_projected=inflows - outflows
        )
