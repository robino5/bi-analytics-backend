from datetime import datetime

from .base import BaseModel, BranchInfoBaseModel

__all__ = ["MarginLoanUsgae", "Exposure", "RMWiseNetTrade", "MarkedInvestor"]


class MarginLoanUsgae(BaseModel):
    perticular: str
    amount: float


class Exposure(BaseModel):
    exposure: str
    investors: int
    loan_amount: float


class RMWiseNetTrade(BranchInfoBaseModel):
    investor_code: str
    opening_balance: float
    ending_balance: float
    net_buysell: float
    rm_name: str


class MarkedInvestor(BaseModel):
    investor_code: str
    branch_code: int
    investor_name: str
    ledger_balance: float
    rm_name: str
    exposure: float
    equity: float
    loan_ratio: str
    marginable_exposure: float | None = None
    marginable_equity: float | None = None
    marginable_loan_ratio: str | None = None
    stock_value: float | None = None
    last_trading_dt: datetime | None = None
    acc_type: str | None = None
    branch_name: str | None = None
