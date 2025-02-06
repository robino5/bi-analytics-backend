from datetime import datetime
from .base import BaseModel, TradingDateModel, PushDateModel

__all__ = ["DailyTurnoverPerformance", "DailyMarginLoanUsage", "SectorExposure","EcrmRetailsRMwise","RMwiseDailyTradeData"]


class DailyTurnoverPerformance(TradingDateModel):
    generated: float | None
    target: float | None


class DailyMarginLoanUsage(TradingDateModel):
    total_allocated: float
    daily_usage: float


class SectorExposure(BaseModel):
    name: str
    value: float

class EcrmRetailsRMwise(BaseModel):
     total_Visits: int | None
     success: int | None
     inProgress: int | None
     discard: int | None
     existingClientVisit: int | None

class RMwiseDailyTradeData(PushDateModel):
     branch_code:float | None
     branch: str | None
     rm_name: str | None
     total_client_today: int | None
     total_turnover_today: float | None


