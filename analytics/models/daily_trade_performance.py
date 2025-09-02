from datetime import datetime
from .base import BaseModel, TradingDateModel, PushDateModel

__all__ = ["DailyTurnoverPerformance", "DailyMarginLoanUsage", "SectorExposure","EcrmRetailsRMwise","RMwiseDailyTradeData","RMWiseLiveSectorData",
           "BranchWiseRMOmsRealtimeSummary"]


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

class RMWiseLiveSectorData(BaseModel):

    branch_code: float
    branch: str 
    rm_name: str
    sector_name: str 
    turnOver: float
    primary_value: float

class BranchWiseRMOmsRealtimeSummary(BaseModel):

    branch_code: int
    rm_name: str
    channel: str
    total_client: int
    trades: int
    total_turnOver: float
    trading_date: datetime
    push_date: datetime





