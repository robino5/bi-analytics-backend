from .base import BranchInfoBaseModel

__all__ = ["RMWiseClientDetail","InvestroLiveNetTradeRMWise"]


class RMWiseClientDetail(BranchInfoBaseModel):
    trader_id: str
    investor_code: str
    join_holder_name: str
    tpv: float
    cv: float
    int_amount: float
    available_cash_balance: float
    loan_balance: float
    equity: float
    exposure_on_equity: float
    daily_turnover: float
    weekly_turnover: float
    fortnightly_turnover: float
    monthly_turnover: float


class InvestroLiveNetTradeRMWise(BranchInfoBaseModel):
    branch_code: int
    branch_name: str
    trader_id: str
    investor_code: str
    join_holder_name: str
    buy: float
    sell: float
    net: float
    ledger_balance: float
