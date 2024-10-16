from .base import BaseModel

__all__ = [
    "ClientSegmentationSummary",
    "BranchWiseClientNumbers",
    "NonPerformerClient",
    "AdminBMClientSegmentationTurnover",
    "AdminBMClientSegmentationTPV",
    "AdminBMClientSegmentationEquity",
    "AdminBMClientSegmentationLedger",
    "AdminMarketShare",
]


class ClientSegmentationSummary(BaseModel):
    customer_category: str
    total_clients: int


class BranchWiseClientNumbers(BaseModel):
    branch_name: str
    branch_code: int
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
