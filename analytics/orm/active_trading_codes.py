from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "ActiveTradingCodeSummaryORM",
    "ActiveTradingCodeDayWiseSummaryORM",
    "ActiveTradingCodeMonthWiseSummaryORM",
    "AdminOMSBranchWiseTurnoverAsOnMonthORM",
    "AdminOMSDateWiseTurnoverORM",
    "AdminSectorWiseTurnoverORM",
    "AdminSectorWiseTurnoverBreakdownORM",
    "AdminRealTimeTurnoverTop20ORM",
    "AdminRealTimeTurnoverComparisonSectorWiseORM",
    "AdminRealTimeTurnoverExchangeTop20ORM",
    "AdminRealTimeTurnoverComparisonTop20SectorWiseORM",
    "AdminOMSBranchWiseTurnoverDtAsOnMonthORM",
    "AdminRegionWiseOMSSummaryORM",
    "AdminRegionWiseDetailsMarketShareLBSLORM",
    "AdminExchangeWiseMarketStatisticsAsOnDateORM",
    "MarketRiskDataORM",
    "MarketRiskDataInvestorDrillDownORM"
]


class BaseActiveTradingOrm(BaseOrm):
    __abstract__ = True

    channel: Mapped[str] = mapped_column("channel", String(50), primary_key=True)
    total_clients: Mapped[int] = mapped_column("Total_Clients", Integer)
    trades: Mapped[int] = mapped_column("Trades", Integer)
    total_turnover: Mapped[float] = mapped_column("Total_turnOver", Numeric(34, 2))
    trading_date: Mapped[datetime] = mapped_column(
        "Trade_dt", DateTime(), primary_key=True
    )

class ActiveTradingCodeSummaryORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_OMS_Summary_data"

    channel: Mapped[str] = mapped_column("channel", String(50), primary_key=True)
    total_clients: Mapped[int] = mapped_column("Total_Clients", Integer)
    trades: Mapped[int] = mapped_column("Trades", Integer)
    total_turnover: Mapped[float] = mapped_column("Total_turnOver", Numeric(34, 2))
    trading_date: Mapped[datetime] = mapped_column(
        "Trade_dt", DateTime(), primary_key=True
    )
    push_date: Mapped[DateTime] = mapped_column(
        "push_date", DateTime(), primary_key=True
    )


class ActiveTradingCodeDayWiseSummaryORM(BaseActiveTradingOrm):
    __tablename__ = "BI_trd_Admin_OMS_DayWise_Summary_data"


class ActiveTradingCodeMonthWiseSummaryORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_OMS_MonthWise_Summary_data"

    channel: Mapped[str] = mapped_column("channel", String(50), primary_key=True)
    total_clients: Mapped[int] = mapped_column("Total_Clients", Integer)
    trades: Mapped[int] = mapped_column("Trades", Integer)
    total_turnover: Mapped[float] = mapped_column("Total_turnOver", Numeric(34, 2))
    month_year = mapped_column("Month_year", String(50), primary_key=True)

class AdminOMSBranchWiseTurnoverAsOnMonthORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_OMS_BranchWise_Turnover_AsonMonth"

    branch_Name: Mapped[str] = mapped_column("branch_Name", String(50), primary_key=True)
    active_clients_today: Mapped[int] = mapped_column("total_client_today", Integer)
    turnover_today: Mapped[float] = mapped_column("total_turnover_today", Numeric(38, 5))
    active_clients_month: Mapped[int] = mapped_column("total_client_Month", Integer)
    turnover_month: Mapped[float] = mapped_column("total_turnover_month", Numeric(38, 5))

class AdminOMSBranchWiseTurnoverDtAsOnMonthORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_OMS_BranchWise_Turnover_AsonMonth_Dt"

    branch_Name: Mapped[str] = mapped_column("branch_Name", String(50), primary_key=True)
    active_clients_today: Mapped[int] = mapped_column("total_client_today", Integer)
    turnover_today: Mapped[float] = mapped_column("total_turnover_today", Numeric(38, 5))
    active_clients_month: Mapped[int] = mapped_column("total_client_Month", Integer)
    turnover_month: Mapped[float] = mapped_column("total_turnover_month", Numeric(38, 5))

class AdminOMSDateWiseTurnoverORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_OMS_DateWise_Turnover"

    active_clients: Mapped[int] = mapped_column("total_client", Integer)
    turnover: Mapped[float] = mapped_column("total_turnover", Numeric(34, 2))
    trading_date: Mapped[datetime] = mapped_column(
        "Trade_dt", DateTime(), primary_key=True
    )

class AdminSectorWiseTurnoverORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_SectorWise"

    name: Mapped[str] = mapped_column("Sector_name", String(50),primary_key=True)
    value: Mapped[float] = mapped_column("TurnOver", Numeric(34, 2))

class AdminSectorWiseTurnoverBreakdownORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_SectorWise_Breakdown"

    sector_name: Mapped[str] = mapped_column("Sector_name", String(50))
    name: Mapped[str] = mapped_column("Com_s_name", String(50),primary_key=True)
    value: Mapped[float] = mapped_column("TurnOver", Numeric(34, 2))

class AdminRealTimeTurnoverTop20ORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_Top_20"

    name: Mapped[str] = mapped_column("Com_s_name", String(50),primary_key=True)
    value: Mapped[float] = mapped_column("TurnOver", Numeric(38, 6))
    buy: Mapped[float] = mapped_column("Buy_TurnOver", Numeric(38, 6))
    sell: Mapped[float] = mapped_column("Sell_TurnOver", Numeric(38, 6))
    trading_date: Mapped[DateTime] = mapped_column("trd_dt", DateTime, primary_key=True)

class AdminRealTimeTurnoverExchangeTop20ORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_Exchange_Top_20"

    name: Mapped[str] = mapped_column("Com_s_name", String(50),primary_key=True)
    value: Mapped[float] = mapped_column("TurnOver", Numeric(38, 6))
    push_date: Mapped[DateTime] = mapped_column(
        "push_date", DateTime(), primary_key=True
    )
    trading_date: Mapped[DateTime] = mapped_column("trd_dt", DateTime, primary_key=True)

class AdminRealTimeTurnoverComparisonSectorWiseORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_SectorWise"

    name: Mapped[str] = mapped_column("Sector_name", String(50),primary_key=True)
    DSE_turnover: Mapped[float] = mapped_column("DSE_turnover", Numeric(38, 6))
    LBSL_turnover: Mapped[float] = mapped_column("TurnOver", Numeric(38, 6))
    trading_date: Mapped[DateTime] = mapped_column("trd_dt", DateTime, primary_key=True)

class AdminRealTimeTurnoverComparisonTop20SectorWiseORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_LBSL_Exchange_Top20_Comparison"

    name: Mapped[str] = mapped_column("Com_s_name", String(50),primary_key=True)
    DSE_turnover: Mapped[float] = mapped_column("DSE_TurnOver", Numeric(38, 6))
    LBSL_turnover: Mapped[float] = mapped_column("LBSL_TurnOver", Numeric(38, 6))
    LBSL_percent: Mapped[float] = mapped_column("Lbsl_Dse_percentage", Numeric(5, 2))
    push_date: Mapped[DateTime] = mapped_column(
        "push_date", DateTime(), primary_key=True
    )
    trading_date: Mapped[DateTime] = mapped_column("trd_dt", DateTime, primary_key=True)

class AdminRegionWiseOMSSummaryORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RegionWise_OMS_Summary_data"

    channel: Mapped[str] = mapped_column("channel", String(50), primary_key=True)
    total_clients: Mapped[int] = mapped_column("Total_Clients", Integer)
    trades: Mapped[int] = mapped_column("Trades", Integer)
    total_turnover: Mapped[float] = mapped_column("Total_turnOver", Numeric(34, 2))
    trading_date: Mapped[datetime] = mapped_column(
        "Trade_dt", DateTime(), primary_key=True
    )
    push_date: Mapped[DateTime] = mapped_column(
        "push_date", DateTime(), primary_key=True
    )
    region_Name: Mapped[str] = mapped_column("Region_Name", String(50), primary_key=True)

class AdminRegionWiseDetailsMarketShareLBSLORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RegionWise_details_market_share_LBSL"

    trading_date: Mapped[DateTime] = mapped_column("trd_dt", DateTime, primary_key=True)
    lbsl_buy_of_dse: Mapped[float] = mapped_column("LBSL BUY of DSE", Numeric(34, 2))
    lbsl_sale_of_dse: Mapped[float] = mapped_column("LBSL SALE of DSE", Numeric(34, 2))
    lbsl_total_of_dse: Mapped[float] = mapped_column(
        "LBSL Total of DSE", Numeric(34, 2)
    )
    dse_market_turnover: Mapped[float] = mapped_column(
        "DSE Market Turnover", Numeric(34, 2)
    )
    lbsl_share_of_dse: Mapped[float] = mapped_column(
        "LBSL Share of DSE", Numeric(34, 2)
    )
    lbsl_buy_of_cse: Mapped[float] = mapped_column("LBSL BUY of CSE", Numeric(34, 2))
    lbsl_sale_of_cse: Mapped[float] = mapped_column("LBSL SALE of CSE", Numeric(34, 2))
    lbsl_total_of_cse: Mapped[float] = mapped_column(
        "LBSL Total of CSE", Numeric(34, 2)
    )
    cse_market_turnover: Mapped[float] = mapped_column(
        "CSE Market Turnover", Numeric(34, 2)
    )
    lbsl_share_of_cse: Mapped[float] = mapped_column(
        "LBSL Share of CSE", Numeric(34, 2)
    )
    lbsl_total_turnover: Mapped[float] = mapped_column(
        "LBSL Total Turnover", Numeric(34, 2)
    )
    exch_total_market: Mapped[float] = mapped_column(
        "EXCH Total Market TO", Numeric(34, 2)
    )
    lbsl_market_all: Mapped[float] = mapped_column(
        "LBSL Market % (DSE+CSE)", Numeric(34, 2)
    )
    foreign: Mapped[float] = mapped_column("Foreign", Numeric(34, 2), default=0)
    net_income: Mapped[float] = mapped_column("Net Income", Numeric(34, 2))
    region_Name: Mapped[str] = mapped_column("region_Name", String(50), primary_key=True)


class AdminExchangeWiseMarketStatisticsAsOnDateORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_ExchangeWise_Market_Statistics_AsOnDate"

    exchange: Mapped[str] = mapped_column("Exchange", String(50), primary_key=True)
    total_turnover: Mapped[float] = mapped_column("total_turnover", Numeric(34, 2))
    avg_turnover: Mapped[float] = mapped_column("avg_turnover", Numeric(34, 2))
    lbsl_total_turnover: Mapped[float] = mapped_column("lbsl_total_turnover", Numeric(34, 2))
    lbsl_avg_turnover: Mapped[float] = mapped_column("lbsl_avg_turnover", Numeric(34, 2))
    count_Total_trade_day: Mapped[int] = mapped_column("count_Total_trade_day", Integer)


class MarketRiskDataORM(BaseOrm):
    __tablename__ = "BI_trd_Market_Risk_data_Analysis"

    symbol: Mapped[str] = mapped_column("Symbol", String(100), primary_key=True)
    risk_level: Mapped[str] = mapped_column("Risk_level", String(50))
    lbs_free_float_salable: Mapped[float] = mapped_column("LBS_free_float_salable", Numeric(34, 2))
    single_scrip_bar: Mapped[float] = mapped_column("Single Scrip bar(%)", Numeric(34, 2))
    buy_qty: Mapped[float] = mapped_column("buy_qty", Numeric(34, 2))
    sell_qty: Mapped[float] = mapped_column("sell_qty", Numeric(34, 2))
    block_pb_contact_today: Mapped[int] = mapped_column("Block/PB contact today", Integer)
    holding_live: Mapped[float] = mapped_column("Holding(live)", Numeric(34, 2))
    free_float_salable: Mapped[float] = mapped_column("FreeFloatShare_Market salable", Numeric(34, 2))
    sector_name: Mapped[str] = mapped_column("SectorName", String(250))
    market_category: Mapped[str] = mapped_column("MarketCategory", String(250))
    dse_30: Mapped[str] = mapped_column("DSE_30", String(2))
    m_loan_listed: Mapped[str] = mapped_column("m_loan_listed", String(10))
    lbs_holding_percent: Mapped[float] = mapped_column("lbs_holding_percent", Numeric(34, 2))
    margin_qty_percentage: Mapped[float] = mapped_column("margin_qty_percentage", Numeric(34, 2))
    third_party_percentage: Mapped[float] = mapped_column("3rd_party_percentage", Numeric(34, 2))
    in_house_transaction: Mapped[float] = mapped_column("In_house_Transaction", Numeric(34, 2))



class MarketRiskDataInvestorDrillDownORM(BaseOrm):
    __tablename__ = "BI_trd_Market_Risk_data_Analysis_investor_Drilldown"
    symbol: Mapped[str] = mapped_column("Symbol", String(100), primary_key=True)
    investor_code: Mapped[str] = mapped_column("investor_code", String(100), primary_key=True)
    investor_name: Mapped[str] = mapped_column("Name", String(100))
    holding_qty: Mapped[float] = mapped_column("Holding(live)", Numeric(34, 2))
    holding_percentage: Mapped[float | None] = mapped_column("lbs_holding_percent", Numeric(34, 2))