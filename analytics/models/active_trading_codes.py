from .base import BaseModel, TradingDateModel

__all__ = [
    "ActiveTradingSummary",
    "ActiveCodeMonthWise",
    "ClientActiveTrading",
    "TradeActiveTrading",
    "TurnoverActiveTrading",
    "AdminOMSBranchWiseTurnoverAsOnMonth",
    "AdminOMSDateWiseTurnover"
]


class ActiveTradingSummary(TradingDateModel):
    channel: str
    total_clients: int
    trades: int
    total_turnover: float


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

