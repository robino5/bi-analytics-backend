from .base import BaseModel, BranchInfoBaseModel,TradingDateModel

__all__ = [
    "ClientSegmentationSummary",
    "BranchWiseClientNumbers",
    "NonPerformerClient",
    "AdminBMClientSegmentationTurnover",
    "AdminBMClientSegmentationTPV",
    "AdminBMClientSegmentationEquity",
    "AdminBMClientSegmentationLedger",
    "AdminMarketShare",
    "AdminGsecTurnover",
    "AdminGsecTurnoverComparison"
]


class ClientSegmentationSummary(BaseModel):
    customer_category: str
    total_clients: int


class BranchWiseClientNumbers(BranchInfoBaseModel):
    total_clients: int
    total_client_percentage: float


class NonPerformerClient(BranchWiseClientNumbers):
    pass


class AdminBMClientSegmentationTurnover(BaseModel):
    customer_category: str
    turnover: float


class AdminBMClientSegmentationTPV(BaseModel):
    customer_category: str
    free_qty: int
    lock_qty: int
    tpv_total: float
    tpv_free_qty_percentage: float
    tpv_lock_qty_percentage: float


class AdminBMClientSegmentationEquity(BaseModel):
    customer_category: str
    equity: float


class AdminBMClientSegmentationLedger(BaseModel):
    customer_category: str
    margin: float


class AdminMarketShare(BaseModel):
    year: int
    month: str
    turnover_dse: float
    turnover_lbsl: float
    trade_percentage: float

class AdminGsecTurnover(TradingDateModel):
    turnover_gsec: float

class AdminGsecTurnoverComparison(TradingDateModel):
    turnover_gsec: float
    turnover:float
