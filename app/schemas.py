from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class DailyChecklistIn(BaseModel):
    trade_date: date
    open_csp_count: Optional[int] = None
    positions_rolled_count: Optional[int] = None
    cash_deployed_pct: Optional[float] = Field(None, ge=0, le=100)
    high_impact_event: Optional[bool] = None
    qqq_rsi_over70: Optional[bool] = None
    notes: Optional[str] = None

class DailyChecklistOut(DailyChecklistIn):
    id: int

class MetricsPreview(BaseModel):
    open_csp_count: int = 0
    any_over_50pct_returned: bool = False
    cash_deployed_pct: float = 0.0
