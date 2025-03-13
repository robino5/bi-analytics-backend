from datetime import datetime
from typing import Optional
from pydantic import field_serializer
from .base import BaseModel, PushDateModel, TradingDateModel

__all__ = [
    "ActiveTradingSummary",
    "ActiveCodeMonthWise",
    "ClientActiveTrading",
    "TradeActiveTrading",
    "TurnoverActiveTrading",
    "AdminOMSBranchWiseTurnoverAsOnMonth",
    "AdminOMSDateWiseTurnover",
    "AdminSectorWiseTurnover",
    "AdminSectorWiseTurnoverBreakdown",
    "AdminRealTimeTurnoverTop20",
    "AdminRealTimeTurnoverComparisonSectorWise",
    "AdminRealTimeTurnoverExchangeTop20",
    "AdminRealTimeTurnoverComparisonTop20SectorWise"
]


class ActiveTradingSummary(TradingDateModel):
    channel: str
    total_clients: int
    trades: int
    total_turnover: float
    push_date: Optional[datetime] = None  # Explicitly mark as Optional

    @field_serializer("push_date")
    def serialize_push_date(self, dt: Optional[datetime], _info) -> str:
        if dt:
            return f"{dt.strftime('%d-%b-%y')} ({dt.strftime('%I:%M:%S %p')})"
        return ""  # Return empty string if push_date is None


class BaseActiveTradingMonthWise(BaseModel):
    month_year: str
    dt: float
    internet: float


class ClientActiveTrading(BaseActiveTradingMonthWise):
    pass


class TradeActiveTrading(BaseActiveTradingMonthWise):
    pass


class TurnoverActiveTrading(BaseActiveTradingMonthWise):
    pass


class ActiveCodeMonthWise(BaseModel):
    channel: str
    month_year: str
    total_clients: int
    total_trades: int
    total_turnover: float

class AdminOMSBranchWiseTurnoverAsOnMonth(BaseModel):
    branch_Name: str
    active_clients_today: int
    turnover_today: float
    active_clients_month: int
    turnover_month: float

class AdminOMSDateWiseTurnover(TradingDateModel):
    active_clients: int
    turnover: float

class AdminSectorWiseTurnover(BaseModel):
    name: str
    value: float

class AdminSectorWiseTurnoverBreakdown(BaseModel):
    sector_name: str
    name: str
    value: float

class AdminRealTimeTurnoverTop20(BaseModel):
    name: str
    value: float

    
class AdminRealTimeTurnoverTop20(BaseModel):
    name: str
    value: float
    buy:float
    sell:float

class AdminRealTimeTurnoverExchangeTop20(PushDateModel):
    name: str
    value: float

class AdminRealTimeTurnoverComparisonSectorWise(TradingDateModel):
    name: str
    primary_value: float
    secondary_value: float

class AdminRealTimeTurnoverComparisonTop20SectorWise(PushDateModel):
    name: str
    primary_value: float
    secondary_value: float
    secondary_percent: float




