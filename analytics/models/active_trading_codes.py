from datetime import datetime

from pydantic import BaseModel as Base
from pydantic import ConfigDict, field_serializer

__all__ = [
    "ActiveTradingSummary",
    "ActiveCodeMonthWise",
    "ClientActiveTrading",
    "TradeActiveTrading",
    "TurnoverActiveTrading",
]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class ActiveTradingSummary(BaseModel):
    channel: str
    total_clients: int
    trades: int
    total_turnover: float
    trading_date: datetime

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%Y")


class BaseActiveTradingMonthWise(BaseModel):
    trading_date: datetime
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
