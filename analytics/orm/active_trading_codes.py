from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "ActiveTradingCodeSummaryORM",
    "ActiveTradingCodeDayWiseSummaryORM",
    "ActiveTradingCodeMonthWiseSummaryORM",
    "AdminOMSBranchWiseTurnoverAsOnMonthORM",
    "AdminOMSDateWiseTurnoverORM"
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


class ActiveTradingCodeSummaryORM(BaseActiveTradingOrm):
    __tablename__ = "BI_trd_Admin_OMS_Summary_data"


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
