from .base import BranchInfoBaseModel

__all__ = [
    "BranchWiseTurnoverStatus",
    "BranchWiseMarginStatus",
    "BranchWiseFundStatus",
    "BranchWiseExposureStatus",
]


class TurnoverCommonAttrModel(BranchInfoBaseModel):
    turnover_daily: float
    turnover_weekly: float
    turnover_monthly: float
    turnover_yearly: float


class BranchWiseTurnoverStatus(TurnoverCommonAttrModel):
    pass


class BranchWiseMarginStatus(TurnoverCommonAttrModel):
    loan_used: float


class BranchWiseFundStatus(BranchInfoBaseModel):
    tpv: float
    total_clients: int
    fund_in: float
    fund_withdrawl: float
    net_fundflow: float


class BranchWiseExposureStatus(BranchInfoBaseModel):
    exposure_type: str
    investors_count: int
    exposure_ratio: float
