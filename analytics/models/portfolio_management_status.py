from .base import BaseModel, TradingDateModel

__all__ = ["DailyNetFundFlow", "TradeVsClient", "PortfolioStatus"]


class DailyNetFundFlow(TradingDateModel):
    amount: float


class TradeVsClient(TradingDateModel):
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
