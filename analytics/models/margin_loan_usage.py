from pydantic import BaseModel as Base
from pydantic import ConfigDict

__all__ = ["MarginLoanUsgae", "Exposure", "RMWiseNetTrade"]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


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
