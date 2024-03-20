from sqlalchemy import Float, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "BranchWiseTurnoverStatusOrm",
    "BranchWiseMarginStatusOrm",
    "BranchWiseFundStatusOrm",
    "BranchWiseMarginExposureStatusOrm",
]


class BranchWiseTurnoverStatusOrm(BaseOrm):
    __tablename__ = "BI_trd_BRANCH_WISE_TURNOVER_STATUS"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    turnover_daily: Mapped[float] = mapped_column(
        "DAILY_TURNOVER", Numeric(34, 2), nullable=False
    )
    turnover_weekly: Mapped[float] = mapped_column(
        "WEEK_TURNOVER", Numeric(34, 2), nullable=False
    )
    turnover_monthly: Mapped[float] = mapped_column(
        "Monthly_TurnOver", Numeric(34, 2), nullable=False
    )
    turnover_yearly: Mapped[float] = mapped_column(
        "Yearly_TurnOver", Numeric(34, 2), nullable=False
    )


class BranchWiseMarginStatusOrm(BaseOrm):
    __tablename__ = "BI_trd_BRANCH_WISE_MARGIN_STATUS"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    loan_used: Mapped[float] = mapped_column(
        "Total_Loan_used", Numeric(34, 2), nullable=False
    )
    turnover_daily: Mapped[float] = mapped_column(
        "DAILY_TURNOVER", Numeric(34, 2), nullable=False
    )
    turnover_weekly: Mapped[float] = mapped_column(
        "WEEK_TURNOVER", Numeric(34, 2), nullable=False
    )
    turnover_monthly: Mapped[float] = mapped_column(
        "Monthly_TurnOver", Numeric(34, 2), nullable=False
    )
    turnover_yearly: Mapped[float] = mapped_column(
        "Yearly_TurnOver", Numeric(34, 2), nullable=False
    )


class BranchWiseFundStatusOrm(BaseOrm):
    __tablename__ = "BI_trd_BRANCH_WISE_FUND_STATUS"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    tpv: Mapped[float] = mapped_column("TPV", Numeric(34, 2), nullable=False)
    total_clients: Mapped[int] = mapped_column("Total_clients", Integer, nullable=False)
    fund_in: Mapped[float] = mapped_column("fund_in", Numeric(34, 2), nullable=False)
    fund_withdrawl: Mapped[float] = mapped_column(
        "fund_withdrawl", Numeric(34, 2), nullable=False
    )
    net_fundflow: Mapped[float] = mapped_column(
        "Net_Fund_Flow", Numeric(34, 2), nullable=False
    )


class BranchWiseMarginExposureStatusOrm(BaseOrm):
    __tablename__ = "BI_trd_Branch_Wise_Margin_Exposure_Status"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    exposure_type: Mapped[str] = mapped_column(
        "Exposure", String(50), nullable=False, primary_key=True
    )
    investors_count: Mapped[int] = mapped_column(
        "Exposure_no_investors", Integer, nullable=False
    )
    exposure_ratio: Mapped[float] = mapped_column(
        "percentage_on_exposure", Float(precision=2), nullable=False
    )
