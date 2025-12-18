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
           "RegionalExposureDetails"
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
    region_name: str
    branch_code: int
    branch_name: str
    total_investor: float
    texpress_investor: float
    ibroker_investor: float
    performer: float
    none_performer: float
    performer_percentage: float
    nonperformer_percentage: float

class RegionalECRMDetails(BaseModel):
    region_name: str
    cluster_name: str
    branch_code: int
    branch_name: str
    total_visits: float
    total_success: float
    total_in_progress: float
    total_discard: float
    total_existing_client_visit: float

class RegionaleKYCDetail(BaseModel):
    region_name: str
    cluster_name: str
    branch_code: int
    branch_name: str
    total_investor: float
    total_submitted: float
    due: float

class RegionalEmployeeStructure(BaseModel):
    region_name: str
    cluster_name: str
    branch_code: int
    branch_name: str
    permanent_trader: float
    contractual_with_salary: float
    contractual_without_salary: float

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
    region_name: str
    cluster_name: str
    branch_code: int
    branch_name: str
    total_party: int
    total_investor: int
    total_turnover: float
    total_commission: float


class RegionalCashMarginDetails(BaseModel):
    region_name: str
    branch_code: int
    branch_name: str
    total_deposit: float
    total_withdrawal: float
    total_portfolio: float
    margin_negative: float
    cash_available: float

class RegionalExposureDetails(BaseModel):
    region_name: str
    branch_code: int
    branch_name: str
    ledger_bal: float
    green: int
    yellow: int
    red: int
    negative_equity: int
