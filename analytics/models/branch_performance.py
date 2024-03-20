from pydantic import BaseModel as Base
from pydantic import ConfigDict

__all__ = [
    "BranchWiseTurnoverStatus",
    "BranchWiseMarginStatus",
    "BranchWiseFundStatus",
    "BranchWiseExposureStatus",
]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class CommonAttributeStatus(BaseModel):
    branch_code: int
    branch_name: str
    turnover_daily: float
    turnover_weekly: float
    turnover_monthly: float
    turnover_yearly: float


class BranchWiseTurnoverStatus(CommonAttributeStatus):
    pass


class BranchWiseMarginStatus(CommonAttributeStatus):
    loan_used: float


class BranchWiseFundStatus(BaseModel):
    branch_code: int
    branch_name: str
    tpv: float
    total_clients: int
    fund_in: float
    fund_withdrawl: float
    net_fundflow: float


class BranchWiseExposureStatus(BaseModel):
    branch_code: int
    branch_name: str
    exposure_type: str
    investors_count: int
    exposure_ratio: float
