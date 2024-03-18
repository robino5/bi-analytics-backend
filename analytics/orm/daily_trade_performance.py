from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "OverallSummaryOrm",
    "DailyTurnoverPerformanceOrm",
    "DailyMarginLoanUsageOrm",
    "SectorExposureCashCodeOrm",
    "SectorExposureMarginCodeOrm",
]


class OverallSummaryOrm(BaseOrm):
    __tablename__ = "BI_trd_BranchWise_Client_Cash_Margin_Details"

    branch_code: Mapped[int] = mapped_column(
        "branch_Code", Numeric(10), primary_key=True
    )
    branch_name: Mapped[str] = mapped_column("branch_Name", String(50))
    total_client: Mapped[float] = mapped_column("Total_client", Integer, nullable=False)
    total_active_client: Mapped[float] = mapped_column(
        "Total_Active_client", Integer, nullable=False
    )
    cash_active_client: Mapped[float] = mapped_column(
        "Cash_active_client", Integer, nullable=False
    )
    margin_active_client: Mapped[float] = mapped_column(
        "Margin_active_client", Integer, nullable=False
    )
    cash_balance: Mapped[float] = mapped_column(
        "Cash_balance", Numeric(38, 2), nullable=True
    )
    cash_stock_balance: Mapped[float] = mapped_column(
        "Cash_Stock_balance", Numeric(38, 2), nullable=False
    )
    cash_daily_turnover: Mapped[float] = mapped_column(
        "Cash_Daily_TurnOver", Numeric(38, 2), nullable=False
    )
    margin_balance: Mapped[float] = mapped_column(
        "Margin_balance", Numeric(38, 2), nullable=True
    )
    margin_stock_balance: Mapped[float] = mapped_column(
        "Margin_Stock_balance", Numeric(38, 2), nullable=False
    )
    margin_daily_turnover: Mapped[float] = mapped_column(
        "Margin_Daily_TurnOver", Numeric(38, 2), nullable=False
    )
    daily_turnover: Mapped[float] = mapped_column(
        "Daily_TurnOver", Numeric(38, 6), nullable=False
    )
    net_buy_sell: Mapped[float] = mapped_column(
        "Net_buy_sell", Numeric(38, 6), nullable=False
    )


class DailyTurnoverPerformanceOrm(BaseOrm):
    __tablename__ = "BI_trd_BranchWise_Daily_TurnOver_TrunOverTarget"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255))
    trading_date: Mapped[datetime] = mapped_column("trd_Dt", DateTime)
    generated: Mapped[float] = mapped_column("Daily_Turnover_generated", Numeric(38, 2))
    target: Mapped[float] = mapped_column("Daily_Turnover_target", Numeric(38, 2))


class DailyMarginLoanUsageOrm(BaseOrm):
    __tablename__ = "BI_trd_Daily_Margin_Loan_Uses"

    branch_code = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name = mapped_column("branch_Name", String(255), nullable=False)
    trading_date = mapped_column("trd_Dt", DateTime, nullable=False)
    loan_amount = mapped_column("Loan_amount", Numeric(38, 2), nullable=False)
    daily_turnover = mapped_column(
        "Daily_TurnOver_Margin_code", Numeric(38, 2), nullable=False
    )
    allocation_ratio = mapped_column(
        "Total_loan_allocation_percentage", Numeric(10, 5), nullable=False
    )


class SectorExposureCashCodeOrm(BaseOrm):
    __tablename__ = "BI_trd_Sector_Exposure_Cash_Codes"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    total_qty: Mapped[float] = mapped_column(
        "Cash_total_qty", Numeric(38, 2), nullable=False
    )
    sector_name: Mapped[str] = mapped_column(
        "Sector_name", String(50), nullable=False, primary_key=True
    )


class SectorExposureMarginCodeOrm(BaseOrm):
    __tablename__ = "BI_trd_Sector_Exposure_Margin_Codes"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    total_qty: Mapped[float] = mapped_column(
        "Cash_total_qty", Numeric(38, 2), nullable=False
    )
    sector_name: Mapped[str] = mapped_column(
        "Sector_name", String(50), nullable=False, primary_key=True
    )
