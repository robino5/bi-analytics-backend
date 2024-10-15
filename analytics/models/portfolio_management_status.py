from datetime import datetime

from pydantic import field_serializer

from .base import BaseModel

__all__ = ["DailyNetFundFlow", "TradeVsClient", "PortfolioStatus"]


class CommonTradingDateModel(BaseModel):
    trading_date: datetime

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%Y")


class DailyNetFundFlow(CommonTradingDateModel):
    amount: float


class TradeVsClient(CommonTradingDateModel):
    active_clients: int
    turnover: float


class TurnoverPerformance(BaseModel):
    name: str
    daily: float
    weekly: float
    monthly: float
    forthnightly: float


class PortfolioStatus(BaseModel):
    perticular: str
    amount: float
