from datetime import datetime
from typing import Optional
from pydantic import field_serializer
from .base import BaseModel, PushDateModel, TradingDateModel

__all__ = [
    "ActiveTradingSummary",
    "ActiveCodeMonthWise",
    "ClientActiveTrading",
    "TradeActiveTrading",
    "TurnoverActiveTrading",
    "AdminOMSBranchWiseTurnoverAsOnMonth",
    "AdminOMSDateWiseTurnover",
    "AdminSectorWiseTurnover",
    "AdminSectorWiseTurnoverBreakdown",
    "AdminRealTimeTurnoverTop20",
    "AdminRealTimeTurnoverComparisonSectorWise",
    "AdminOMSBranchWiseTurnoverDtAsOnMonth",
    "AdminRealTimeTurnoverExchangeTop20",
    "AdminRealTimeTurnoverComparisonTop20SectorWise",
    "AdminRegionWiseOMSSummary",
    "AdminRegionWiseDetailsMarketShareLBSL",
    "AdminExchangeWiseMarketStatisticsAsOnDate",
    "MarketRiskData",
    "MarketRiskDataInvestorDrillDown"
]


class ActiveTradingSummary(TradingDateModel):
    channel: str
    total_clients: int
    trades: int
    total_turnover: float
    push_date: Optional[datetime] = None  # Explicitly mark as Optional

    @field_serializer("push_date")
    def serialize_push_date(self, dt: Optional[datetime], _info) -> str:
        if dt:
            return f"{dt.strftime('%d-%b-%y')} ({dt.strftime('%I:%M:%S %p')})"
        return ""  # Return empty string if push_date is None


class BaseActiveTradingMonthWise(BaseModel):
    month_year: str
    dt: float
    internet: float


class ClientActiveTrading(BaseActiveTradingMonthWise):
    pass


class TradeActiveTrading(BaseActiveTradingMonthWise):
    pass


class TurnoverActiveTrading(BaseActiveTradingMonthWise):
    pass


class ActiveCodeMonthWise(BaseModel):
    channel: str
    month_year: str
    total_clients: int
    total_trades: int
    total_turnover: float

class AdminOMSBranchWiseTurnoverAsOnMonth(BaseModel):
    branch_Name: str
    active_clients_today: int
    turnover_today: float
    active_clients_month: int
    turnover_month: float

class AdminOMSBranchWiseTurnoverDtAsOnMonth(BaseModel):
    branch_Name: str
    active_clients_today: int
    turnover_today: float
    active_clients_month: int
    turnover_month: float

class AdminOMSDateWiseTurnover(TradingDateModel):
    active_clients: int
    turnover: float

class AdminSectorWiseTurnover(BaseModel):
    name: str
    value: float

class AdminSectorWiseTurnoverBreakdown(BaseModel):
    sector_name: str
    name: str
    value: float

class AdminRealTimeTurnoverTop20(BaseModel):
    name: str
    value: float

    
class AdminRealTimeTurnoverTop20(TradingDateModel):
    name: str
    value: float
    buy:float
    sell:float

class AdminRealTimeTurnoverExchangeTop20(TradingDateModel):
    name: str
    value: float
    push_date: Optional[datetime] = None 

    @field_serializer("push_date")
    def serialize_push_date(self, dt: Optional[datetime], _info) -> str:
        if dt:
            return f"{dt.strftime('%d-%b-%y')} ({dt.strftime('%I:%M:%S %p')})"
        return ""  

class AdminRealTimeTurnoverComparisonSectorWise(TradingDateModel):
    name: str
    DSE_turnover: float
    LBSL_turnover: float

class AdminRealTimeTurnoverComparisonTop20SectorWise(TradingDateModel):
    name: str
    DSE_turnover: float
    LBSL_turnover: float
    LBSL_percent: float
    push_date: Optional[datetime] = None 

    @field_serializer("push_date")
    def serialize_push_date(self, dt: Optional[datetime], _info) -> str:
        if dt:
            return f"{dt.strftime('%d-%b-%y')} ({dt.strftime('%I:%M:%S %p')})"
        return ""
    
class AdminRegionWiseOMSSummary(TradingDateModel):
    channel: str
    total_clients: int
    trades: int
    total_turnover: float
    region_Name: str
    push_date: Optional[datetime] = None  # Explicitly mark as Optional

    @field_serializer("push_date")
    def serialize_push_date(self, dt: Optional[datetime], _info) -> str:
        if dt:
            return f"{dt.strftime('%d-%b-%y')} ({dt.strftime('%I:%M:%S %p')})"
        return ""  # Return empty string if push_date is None
  
class AdminRegionWiseDetailsMarketShareLBSL(TradingDateModel):
    llbsl_buy_of_dse: float | None = None
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
    region_Name: str | None = None


class AdminExchangeWiseMarketStatisticsAsOnDate(BaseModel):
    exchange: str
    total_turnover: float
    avg_turnover: float
    lbsl_total_turnover: float
    lbsl_avg_turnover: float
    count_Total_trade_day: int

class MarketRiskData(BaseModel):
    symbol: str
    risk_level: str
    lbs_free_float_salable: float
    single_scrip_bar: float
    buy_qty: float
    sell_qty: float
    block_pb_contact_today: int
    holding_live: float
    free_float_salable: float
    sector_name: str
    market_category: str
    dse_30: str
    m_loan_listed: str
    lbs_holding_percent: float
    margin_qty_percentage: float
    third_party_percentage: float
    in_house_transaction: float

class MarketRiskDataInvestorDrillDown(BaseModel):
    symbol: str
    investor_code: str
    investor_name: str
    holding_qty: float
    holding_percentage: float | None




