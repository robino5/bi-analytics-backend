from datetime import datetime
from .base import BaseModel

__all__ = ["ExchangeWisearketStatistics", 
           "BranchWisearketStatistics",
           "RegionalClientPerformanceNonPerformance",
           "RegionalECRMDetails",
           "RegionalECRMDetails",
           "RegionaleKYCDetail",
           "RegionalEmployeeStructure",
           "RegionalChannelWiseTrades",
           "RegionalPartyTurnoverCommission",
           "RegionalCashMarginDetails",
           "RegionalExposureDetails",
           "RegionalBusinessPerformance",
           "RegionalOfficeSpace"
           ]

class ExchangeWisearketStatistics(BaseModel):
    exchange: str
    total_turnover: float
    avg_turnover: float
    lbsl_total_turnover: float
    lbsl_avg_turnover: float

class BranchWisearketStatistics(BaseModel):
    region_id: int
    region_name: str
    branch_code: int
    branch_name: str
    exchange: str
    total_turnover: float
    avg_turnover: float

class RegionalClientPerformanceNonPerformance(BaseModel):
    region_name: str | None=None
    cluster_name: str | None=None
    branch_code: int | None=None
    branch_name: str | None=None
    total_investor: float | None=0
    texpress_investor: float | None=0
    ibroker_investor: float | None=0
    performer: float | None=0
    none_performer: float | None=0
    performer_percentage: float | None=0
    nonperformer_percentage: float | None=0

class RegionalECRMDetails(BaseModel):
    region_name: str | None=None
    cluster_name: str | None=None
    branch_code: int | None=None
    branch_name: str | None=None
    total_visits: float | None=0
    total_success: float | None=0
    total_in_progress: float | None=0
    total_discard: float | None=0
    total_existing_client_visit: float | None=0

class RegionaleKYCDetail(BaseModel):
    region_name: str | None=None
    cluster_name: str | None=None
    branch_code: int | None=None
    branch_name: str | None=None
    total_investor: float | None=0
    total_submitted: float | None=0
    due: float | None=0

class RegionalEmployeeStructure(BaseModel):
    region_name: str | None=None
    cluster_name: str | None=None
    branch_code: int | None=None
    branch_name: str | None=None
    permanent_trader: float | None=0
    contractual_with_salary: float | None=0
    contractual_without_salary: float | None=0

class RegionalChannelWiseTrades(BaseModel):
    region_name: str
    branch_code: int
    branch_name: str
    channel: str
    total_clients: int
    total_trades: int
    total_turnover: float
    push_date: datetime

class RegionalPartyTurnoverCommission(BaseModel):
    region_name: str | None=None
    cluster_name: str | None=None
    branch_code: int | None=None
    branch_name: str | None=None
    total_party: int | None=0
    total_investor: int | None=0
    total_turnover: float | None=0
    total_commission: float | None=0


class RegionalCashMarginDetails(BaseModel):
    region_name: str | None=None
    branch_code: int | None=None
    branch_name: str | None=None
    total_deposit: float | None=0
    total_withdrawal: float | None=0
    total_portfolio: float | None=0
    margin_negative: float | None=0
    cash_available: float | None=0

class RegionalExposureDetails(BaseModel):
    region_name: str | None=None
    branch_code: int | None=None
    branch_name: str | None=None
    ledger_bal: float | None=0
    green: int | None=0
    yellow: int | None=0
    red: int | None=0
    negative_equity: int | None=0


class RegionalBusinessPerformance(BaseModel):

    region_name: str
    cluster_name: str
    branch_code: int
    branch_name: str
    target: float
    turnover_achieved: float
    turnover_percentage: float
    fund_target: float
    total_net_fund: float
    total_net_link_share: float
    fund_percentage: float
    bo_opening_target: float
    bo_opened: float
    bo_percentage: float
    total_trade_days: int
    commission: float
    total_link_share_in: float
    total_link_share_out: float
    total_deposit: float
    total_withdrawal: float
    total_expenses: float
    profit_loss: float

class RegionalOfficeSpace(BaseModel):
    region_name: str | None=None
    branch_code: int | None=None
    branch_name: str | None=None
    office_space: float | None=0