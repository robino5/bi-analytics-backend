from datetime import datetime

from pydantic import BaseModel as Base
from pydantic import ConfigDict, field_serializer

__all__ = ["DailyNetFundFlow", "TradeVsClient", "PortfolioStatus"]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class DailyNetFundFlow(BaseModel):
    trading_date: datetime
    amount: float

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%Y")


class TradeVsClient(BaseModel):
    trading_date: datetime
    active_clients: int
    turnover: float

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%Y")


class TurnoverPerformance(BaseModel):
    name: str
    daily: float
    weekly: float
    monthly: float
    forthnightly: float


class PortfolioStatus(BaseModel):
    perticular: str
    amount: float
