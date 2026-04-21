# backend/services/scenario_simulator.py
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel
from backend.services.wealth_mapper import WealthMapper

class YearlyProjection(BaseModel):
    year: int
    net_worth: float
    invested: float
    returns_earned: float

class ScenarioResult(BaseModel):
    scenario_name: str
    yearly_projections: List[YearlyProjection]
    goal_completion_date: Optional[date]
    total_wealth_at_year_n: float
    vs_base_case_delta: float

class ChartSeries(BaseModel):
    scenario_name: str
    color: str
    data: List[float]

class ChartData(BaseModel):
    x_axis: List[int]
    series: List[ChartSeries]

class MultiScenarioResult(BaseModel):
    scenarios: List[ScenarioResult]
    chart_data: ChartData
    cost_of_inaction: float
    cost_of_inaction_message: str

class Adjustment(BaseModel):
    type: str # increase_sip, reduce_spend, add_lump_sum, change_income
    amount: float
    category: Optional[str] = None

class ScenarioInput(BaseModel):
    scenario_name: str
    base_monthly_savings: float
    adjustments: List[Adjustment]
    projection_years: int
    goal_id: Optional[int] = None

class ScenarioSimulator:
    
    async def run_scenario(self, user_id: int, scenario: ScenarioInput, base_result: Optional[ScenarioResult] = None) -> ScenarioResult:
        mapper = WealthMapper()
        snapshot = await mapper.get_wealth_snapshot(user_id)
        
        starting_wealth = snapshot.net_worth
        monthly_savings = scenario.base_monthly_savings
        
        # Apply adjustments
        lump_sum = 0
        for adj in scenario.adjustments:
            if adj.type == "add_lump_sum":
                lump_sum += adj.amount
            elif adj.type == "increase_sip":
                monthly_savings += adj.amount
            elif adj.type == "reduce_spend":
                monthly_savings += adj.amount
            elif adj.type == "change_income":
                monthly_savings += adj.amount
        
        starting_wealth += lump_sum
        
        annual_return = 0.10 # Default 10%
        projections = []
        current_wealth = starting_wealth
        current_invested = starting_wealth # Simplified
        
        for year in range(1, scenario.projection_years + 1):
            for _ in range(12):
                interest = current_wealth * (annual_return / 12)
                current_wealth += interest + monthly_savings
                current_invested += monthly_savings
                
            projections.append(YearlyProjection(
                year=year,
                net_worth=current_wealth,
                invested=current_invested,
                returns_earned=current_wealth - current_invested
            ))
            
        delta = current_wealth - base_result.total_wealth_at_year_n if base_result else 0
        
        return ScenarioResult(
            scenario_name=scenario.scenario_name,
            yearly_projections=projections,
            goal_completion_date=None,
            total_wealth_at_year_n=current_wealth,
            vs_base_case_delta=delta
        )

    async def run_multi_scenario(self, user_id: int, scenarios_in: List[ScenarioInput]) -> MultiScenarioResult:
        results = []
        base_scenario = scenarios_in[0]
        base_res = await self.run_scenario(user_id, base_scenario)
        results.append(base_res)
        
        for s_in in scenarios_in[1:]:
            res = await self.run_scenario(user_id, s_in, base_res)
            results.append(res)
            
        # Chart Data
        years = list(range(1, base_scenario.projection_years + 1))
        colors = ["#0A1628", "#00D4AA", "#F5A623", "#3182CE"]
        series = []
        for i, res in enumerate(results):
            series.append(ChartSeries(
                scenario_name=res.scenario_name,
                color=colors[i % len(colors)],
                data=[p.net_worth for p in res.yearly_projections]
            ))
            
        best_wealth = max(r.total_wealth_at_year_n for r in results)
        cost_of_inaction = best_wealth - base_res.total_wealth_at_year_n
        
        return MultiScenarioResult(
            scenarios=results,
            chart_data=ChartData(x_axis=years, series=series),
            cost_of_inaction=cost_of_inaction,
            cost_of_inaction_message=f"Doing nothing costs you ₹{cost_of_inaction:,.0f} over {base_scenario.projection_years} years compared to your best option."
        )
