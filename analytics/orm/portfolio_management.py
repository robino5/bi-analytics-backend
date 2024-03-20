from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "DailyNetFundFlowOrm",
    "TurnoverAndClientsTradeOrm",
    "TurnoverPerformanceOrm",
    "AccountOpeningFundInOutFlowOrm",
    "PortfolioManagementStatusOrm",
]


class DailyNetFundFlowOrm(BaseOrm):
    __tablename__ = "BI_trd_Daily_Net_Fund_Flow"

    branch_code: Mapped[int] = mapped_column(
        "branch_Code", Integer, nullable=False, primary_key=True
    )
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    fundflow: Mapped[float] = mapped_column(
        "Net_fundFlow", Numeric(34, 0), nullable=False
    )
    trading_date: Mapped[datetime] = mapped_column(
        "trans_Dt", DateTime(), nullable=False, primary_key=True
    )


class TurnoverAndClientsTradeOrm(BaseOrm):
    __tablename__ = "BI_trd_Graph_BranchTurnover_TradedClient"

    branch_code = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name = mapped_column("branch_Name", String(255), nullable=False)
    trading_date = mapped_column("trd_dt", DateTime(), nullable=False, primary_key=True)
    active_client = mapped_column("active_client", Numeric(5, 0), nullable=False)
    turnover = mapped_column("TurnOver", Numeric(34, 0), nullable=False)


class TurnoverPerformanceOrm(BaseOrm):
    __tablename__ = "BI_trd_Turnover_Performance"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    col3: Mapped[str] = mapped_column("col3", String(50), primary_key=True)
    col2: Mapped[str] = mapped_column("col2", String(50), primary_key=True)
    col1: Mapped[float] = mapped_column("col1", Numeric(38, 2), nullable=False)


class AccountOpeningFundInOutFlowOrm(BaseOrm):
    __tablename__ = "BI_trd_Account_Opening_Fund_InOutFlow"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    col3: Mapped[str] = mapped_column("col3", String(50), primary_key=True)
    col2: Mapped[str] = mapped_column("col2", String(50), primary_key=True)
    col1: Mapped[float] = mapped_column("col1", Numeric(38, 2), nullable=False)


class PortfolioManagementStatusOrm(BaseOrm):
    __tablename__ = "BI_trd_Portfolio_Management_Status"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255), nullable=False)
    perticular = mapped_column("Perticular", String(50), primary_key=True)
    amount = mapped_column("Amount", Numeric(38, 4), nullable=False)
