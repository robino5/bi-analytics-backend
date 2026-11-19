from .base import BaseModel 

__all__ = [
    "MarketSpotDataInvestorDrillDown",
    "MarketZGroupDataInvestorDrillDown"
]

class MarketSpotDataInvestorDrillDown(BaseModel):
    symbol: str
    investor_code: str
    investor_name: str
    account_type: str
    current_balance: float
    ledger_balance: float
    spot_buy_qty: float
    spot_buy_amount: float
    cash_deposit: float
    non_cash_deposit: float
    used_excess_lbsl_fund: float
    fund_using_level: str
    rm_branch: str
    rm_name: str

class MarketZGroupDataInvestorDrillDown(BaseModel):
    symbol: str
    investor_code: str
    investor_name: str
    account_type: str
    current_balance: float
    ledger_balance: float
    z_buy_qty: float
    z_buy_amount: float
    cash_deposit: float
    non_cash_deposit: float
    used_excess_lbsl_fund: float
    fund_using_level: str
    rm_branch: str
    rm_name: str