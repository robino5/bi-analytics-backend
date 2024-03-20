from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "MarginLoanAllocationUsageOrm",
    "ExposureControllingManagementOrm",
    "RMWiseNetTradeOrm",
    "RedZoneInvestorOrm",
    "YellowZoneInvestorOrm",
    "NegativeEquityInvestorOrm",
]


class BaseInvestor(BaseOrm):
    """Base Investor Type Model class with common attributes for Red, Yellow & Negative Equity Clients"""

    __abstract__ = True

    investor_code: Mapped[str] = mapped_column(
        "investor_code", String(50), primary_key=True
    )
    branch_code: Mapped[int] = mapped_column("branch_code", Integer, primary_key=True)
    investor_name: Mapped[str] = mapped_column(
        "investor_name", String(255), nullable=False
    )
    ledger_balance: Mapped[float] = mapped_column(
        "Ledger_balance", Numeric(34, 2), nullable=False
    )
    rm_name: Mapped[str] = mapped_column("RM_NAME", String(50), nullable=False)


class MarginLoanAllocationUsageOrm(BaseOrm):
    __tablename__ = "BI_trd_Margin_Loan_Allocation_Uses"
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    col2: Mapped[str] = mapped_column("col2", String(88), nullable=False)
    col1: Mapped[float] = mapped_column("col1", Numeric(34, 2), nullable=False)


class ExposureControllingManagementOrm(BaseOrm):
    __tablename__ = "BI_trd_Exposure_Controlling_Management"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    exposure_type: Mapped[str] = mapped_column("Exposure", String(88), nullable=False)
    investors_count: Mapped[int] = mapped_column(
        "Exposure_no_investors", Numeric(10, 4), nullable=False
    )
    loan_amount: Mapped[float] = mapped_column(
        "Loan_amount", Numeric(34, 2), nullable=False
    )


class RMWiseNetTradeOrm(BaseOrm):
    __tablename__ = "BI_trd_RM_Investors_NetTrade"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    investor_code: Mapped[str] = mapped_column(
        "investor_code", String(50), nullable=False
    )
    opening_balance: Mapped[float] = mapped_column(
        "Opening_balance", Numeric(34, 2), nullable=False
    )
    ending_balance: Mapped[float] = mapped_column(
        "Ending_balance", Numeric(34, 2), nullable=False
    )
    net_buysell: Mapped[float] = mapped_column(
        "Net_buy_sell", Numeric(34, 2), nullable=False
    )
    rm_name: Mapped[str] = mapped_column("RM_NAME", String(50), nullable=False)


class RedZoneInvestorOrm(BaseInvestor):
    __tablename__ = "BI_trd_RM_Investors_Red_zone"


class YellowZoneInvestorOrm(BaseInvestor):
    __tablename__ = "BI_trd_RMWise_Investors_Yellow_zone"


class NegativeEquityInvestorOrm(BaseInvestor):
    __tablename__ = "BI_trd_Branch_NegativeEquity_codes"
