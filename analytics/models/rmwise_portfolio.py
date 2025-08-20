from .base import BaseModel

__all__ = ["PortfolioMangement","RmPerformanceSummary"]


class PortfolioMangement(BaseModel):
    particular: str
    amount: float

class RmPerformanceSummary(BaseModel):
    branch_code: int | None
    branch_name: str | None
    trader_id: str | None =None
    trader_name: str | None =None
    emp_number: str | None =None
    yearly_bo: float | None =None
    yearly_fund: float | None = None
    daily_traded: float | None = None
    commission: float | None = None
    new_bo: float | None = None
    total_link_share_in: float | None = None
    total_link_share_out: float | None = None
    total_net_link_share: float | None = None
    total_deposit: float | None = None
    total_withdrawal: float | None = None
    total_net_fund: float | None = None
    region_name: str | None = None
    cluster_name: str | None = None
