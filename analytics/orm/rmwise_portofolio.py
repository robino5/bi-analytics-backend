from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "RMWiseFundCollectionOrm",
    "RMWisePortfolioMangementORM",
    "RMWiseDailyNetFundFlowORM",
    "RMWiseRedZoneTraderORM",
    "RMWiseYellowZoneTraderORM",
]


class RMWiseFundCollectionOrm(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Account_Opening_Fund_InOutFlow"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    trader_id: Mapped[str] = mapped_column(String(50))
    trader_name: Mapped[str] = mapped_column(String(50))
    col3: Mapped[str] = mapped_column("col3", String(50), primary_key=True)
    col2: Mapped[str] = mapped_column("col2", String(50), primary_key=True)
    col1: Mapped[float] = mapped_column("col1", Numeric(34, 2))


class RMWisePortfolioMangementORM(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Portfolio_Management_Status"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    trader_id: Mapped[str] = mapped_column("trader_id", String(50), primary_key=True)
    trader_name: Mapped[str] = mapped_column("trader_name", String(50))
    particular_type: Mapped[str] = mapped_column(
        "Perticular", String(50), primary_key=True
    )
    amount: Mapped[float] = mapped_column("Amount", Numeric(34, 2))


class RMWiseDailyNetFundFlowORM(BaseOrm):
    __tablename__ = "BI_trd_RMWise_Daily_Net_Fund_Flow"

    branch_code: Mapped[int] = mapped_column("Branch_Code", Integer, primary_key=True)
    trader_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    trader_name: Mapped[str] = mapped_column(String(50))
    fundflow: Mapped[float] = mapped_column("Net_fund_Flow", Numeric(34, 2))
    trading_date: Mapped[datetime] = mapped_column(
        "trans_dt", DateTime, primary_key=True
    )


class ZoneWiseTraderAbastractOrm(BaseOrm):
    __abstract__ = True

    branch_name: Mapped[str] = mapped_column("Branch_Name", String(50))
    branch_code: Mapped[int] = mapped_column("Branch_Code", Integer, primary_key=True)
    investor_code: Mapped[str] = mapped_column(String(255), primary_key=True)
    investor_name: Mapped[str] = mapped_column(String(255))
    ledger_balance: Mapped[float] = mapped_column("Ledger_balance", Numeric(34, 2))
    rm_name: Mapped[str] = mapped_column("RM_NAME", String(255), primary_key=True)


class RMWiseRedZoneTraderORM(ZoneWiseTraderAbastractOrm):
    __tablename__ = "BI_trd_RMWise_Investors_Red_zone"


class RMWiseYellowZoneTraderORM(ZoneWiseTraderAbastractOrm):
    __tablename__ = "BI_trd_RMWise_Investors_Yellow_zone"
