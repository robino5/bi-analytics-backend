from datetime import datetime

from pydantic import BaseModel as Base
from pydantic import ConfigDict, field_serializer

__all__ = [
    "BoardTurnOver",
    "BoardTurnOverBreakdown",
    "MarketShareLBSL",
    "ATBMarketShareSME",
    "CompanyWiseSaleableStock",
    "InvestorWiseSaleableStock",
    "CompanyWiseSaleableStockPercentage"
]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class BoardTurnOver(BaseModel):
    trading_date: datetime
    board: str
    turnover: float
    dse_percentage: float
    lbsl_turnover: float
    lbsl_percentage: float

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%Y")


class BoardTurnOverBreakdown(BoardTurnOver):
    pass


class MarketShareLBSL(BaseModel):
    trading_date: datetime
    lbsl_buy_of_dse: float | None = None
    lbsl_sale_of_dse: float | None = None
    lbsl_total_of_dse: float | None = None
    dse_market_turnover: float | None = None
    lbsl_share_of_dse: float | None = None
    lbsl_buy_of_cse: float | None = None
    lbsl_sale_of_cse: float | None = None
    lbsl_total_of_cse: float | None = None
    cse_market_turnover: float | None = None
    lbsl_share_of_cse: float | None = None
    lbsl_total_turnover: float | None = None
    exch_total_market: float | None = None
    lbsl_market_all: float | None = None
    foreign: float | None = None
    net_income: float | None = None

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%Y")


class ATBMarketShareSME(BaseModel):
    trading_date: datetime
    dse_sme_turnover: float | None = None
    dse_atb_turnover: float | None = None
    dse_gsec_turnover: float | None = None
    dse_block_turnover: float | None = None
    sme_percent: float | None = None
    atb_percent: float | None = None
    cse_sme_turnover: float | None = None
    cse_atb_turnover: float | None = None
    cse_gsec_turnover: float | None = None
    cse_block_turnover: float | None = None
    cse_sme_percent: float | None = None
    cse_atb_percent: float | None = None

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%Y")


class CompanyWiseSaleableStock(BaseModel):
    company_name: str
    stock_available: int


class InvestorWiseSaleableStock(BaseModel):
    compnay_name: str
    branch_name: str
    investor_code: str
    client_name: str
    rm_name: str
    stock_available: int


class CompanyWiseSaleableStockPercentage(BaseModel):
    compnay_name: str
    branch_name: str
    stock_available: int
    stock_available_percentage: float
