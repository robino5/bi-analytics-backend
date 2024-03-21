from pydantic import BaseModel as Base
from pydantic import ConfigDict

__all__ = ["RMWiseClientDetail"]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class RMWiseClientDetail(BaseModel):
    branch_code: int
    branch_name: str
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
