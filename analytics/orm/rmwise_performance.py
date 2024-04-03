from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = ["RMWiseTurnoverPerformanceOrm", "RMWiseClientDetailOrm"]


class RMWiseTurnoverPerformanceOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Turnover_Performance"

    branch_name: Mapped[str] = mapped_column("BRANCH_NAME", String(50))
    branch_code: Mapped[int] = mapped_column("BRANCH_CODE", Integer, primary_key=True)
    trader_id: Mapped[str] = mapped_column(String(50))
    trader_name: Mapped[str] = mapped_column(String(50))
    col3: Mapped[str] = mapped_column("col3", String(50), primary_key=True)
    col2: Mapped[str] = mapped_column("col2", String(50), primary_key=True)
    col1: Mapped[float] = mapped_column("col1", Numeric(2))


class RMWiseClientDetailOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Client_Details"

    branch_code: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column(String(50), nullable=False)
    trader_id: Mapped[str] = mapped_column(String(50))
    investor_code: Mapped[str] = mapped_column(String(50), primary_key=True)
    join_holder_name: Mapped[str] = mapped_column("f_Join_Holder_Name", String(50))
    tpv: Mapped[float] = mapped_column("TPV", Numeric(2))
    cv: Mapped[float] = mapped_column("CV", Numeric(2))
    int_amount: Mapped[float] = mapped_column("Int_Amount", Numeric(2))
    available_cash_balance: Mapped[float] = mapped_column(
        "Available_cash_bal", Numeric(2)
    )
    loan_balance: Mapped[float] = mapped_column("Loan_bal", Numeric(2))
    equity: Mapped[float] = mapped_column("Equity", Numeric(2))
    exposure_on_equity: Mapped[float] = mapped_column("exposure_on_Equity", Numeric(2))
    daily_turnover: Mapped[float] = mapped_column("Daily_TurnOver", Numeric(2))
    weekly_turnover: Mapped[float] = mapped_column("Weekly_TurnOver", Numeric(2))
    fortnightly_turnover: Mapped[float] = mapped_column(
        "Fortnightly_TurnOver", Numeric(2)
    )
    monthly_turnover: Mapped[float] = mapped_column("Monthly_TurnOver", Numeric(2))
