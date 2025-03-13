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
    "AdminRealTimeTurnoverComparisonTop20SectorWiseORM"
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

class AdminRealTimeTurnoverExchangeTop20ORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_Exchange_Top_20"

    name: Mapped[str] = mapped_column("Com_s_name", String(50),primary_key=True)
    value: Mapped[float] = mapped_column("TurnOver", Numeric(38, 6))
    push_date: Mapped[DateTime] = mapped_column(
        "push_date", DateTime(), primary_key=True
    )

class AdminRealTimeTurnoverComparisonSectorWiseORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_SectorWise"

    name: Mapped[str] = mapped_column("Sector_name", String(50),primary_key=True)
    primary_value: Mapped[float] = mapped_column("DSE_turnover", Numeric(38, 6))
    secondary_value: Mapped[float] = mapped_column("TurnOver", Numeric(38, 6))
    trading_date: Mapped[DateTime] = mapped_column("trd_dt", DateTime, primary_key=True)

class AdminRealTimeTurnoverComparisonTop20SectorWiseORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_LBSL_Exchange_Top20_Comparison"

    name: Mapped[str] = mapped_column("Com_s_name", String(50),primary_key=True)
    primary_value: Mapped[float] = mapped_column("DSE_TurnOver", Numeric(38, 6))
    secondary_value: Mapped[float] = mapped_column("LBSL_TurnOver", Numeric(38, 6))
    secondary_percent: Mapped[float] = mapped_column("Lbsl_Dse_percentage", Numeric(5, 2))
    push_date: Mapped[DateTime] = mapped_column(
        "push_date", DateTime(), primary_key=True
    )
