from .base import BaseModel

__all__ = ["MarginLoanUsgae", "Exposure", "RMWiseNetTrade", "MarkedInvestor"]


class MarginLoanUsgae(BaseModel):
    perticular: str
    amount: float


class Exposure(BaseModel):
    exposure: str
    investors: int
    loan_amount: float


class RMWiseNetTrade(BaseModel):
    branch_code: int
    branch_name: str
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
