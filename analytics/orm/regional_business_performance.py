
from sqlalchemy import  DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from db import BaseOrm

__all__ = [
    "BranchWisearketStatisticsORM", 
    "ExchangeWisearketStatisticsORM" ,
    "RegionalClientPerformanceNonPerformanceORM",
    "RegionalECRMDetailsORM",
    "RegionaleKYCDetailORM",
    "RegionalEmployeeStructureORM",
    "RegionalChannelWiseTradesORM",
    "RegionalPartyTurnoverCommissionORM",
    "RegionalCashMarginDetailsORM",
    ]

class ExchangeWisearketStatisticsORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_ExchangeWise_Market_Statistics"

    exchange: Mapped[str] = mapped_column("exchange", String(50), primary_key=True)
    total_turnover: Mapped[float] = mapped_column("total_turnover", Numeric(34, 0), nullable=False)
    avg_turnover: Mapped[float] = mapped_column("avg_turnover", Numeric(34, 0), nullable=False)
    lbsl_total_turnover: Mapped[float] = mapped_column("lbsl_total_turnover", Numeric(34, 0), nullable=False)
    lbsl_avg_turnover: Mapped[float] = mapped_column("lbsl_avg_turnover", Numeric(34, 0), nullable=False)


class BranchWisearketStatisticsORM(BaseOrm):
    __tablename__ = "BI_trd_Admin_BranchWise_Market_Statistics"

    region_id: Mapped[int] = mapped_column("region_id", Integer, primary_key=True)
    region_name: Mapped[str] = mapped_column("region_name", String(15))
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(50))
    exchange: Mapped[str] = mapped_column("exchange", String(50))
    total_turnover: Mapped[float] = mapped_column("total_turnover", Numeric(34, 0), nullable=False)
    avg_turnover: Mapped[float] = mapped_column("avg_turnover", Numeric(34, 0), nullable=False)


class RegionalClientPerformanceNonPerformanceORM(BaseOrm):
    __tablename__ = "BI_trd_Regional_Client_Performance_NonPerformance"

    region_name: Mapped[str] = mapped_column("region_Name", String(50), primary_key=True)
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(50))
    total_investor: Mapped[float] = mapped_column("BranchWise_Total_Investor", Numeric(34, 0), nullable=False)
    texpress_investor: Mapped[float] = mapped_column("BranchWise_Texpress_Investor", Numeric(34, 0), nullable=False)
    ibroker_investor: Mapped[float] = mapped_column("BranchWise_Ibroker_Investor", Numeric(34, 0), nullable=False)
    performer: Mapped[float] = mapped_column("BranchWise_performer", Numeric(34, 0), nullable=False)
    none_performer: Mapped[float] = mapped_column("BranchWise_nonperformer", Numeric(34, 0), nullable=False)
    performer_percentage: Mapped[float] = mapped_column("Performer_Percentage", Numeric(34, 0), nullable=False)
    nonperformer_percentage: Mapped[float] = mapped_column("NonPerformer_Percentage", Numeric(34, 0), nullable=False)


class RegionalECRMDetailsORM(BaseOrm):
    __tablename__ = "BI_trd_Regional_ECRM_Details"

    region_name: Mapped[str] = mapped_column("Region", String(50), primary_key=True)
    cluster_name: Mapped[str] = mapped_column("Cluster", String(50))
    branch_code: Mapped[int] = mapped_column("branch_code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("Branch", String(50))
    total_visits: Mapped[float] = mapped_column("Total_Visits", Numeric(34, 0), nullable=False)
    total_success: Mapped[float] = mapped_column("Success", Numeric(34, 0), nullable=False)
    total_in_progress: Mapped[float] = mapped_column("InProgress", Numeric(34, 0), nullable=False)
    total_discard: Mapped[float] = mapped_column("Discard", Numeric(34, 0), nullable=False)
    total_existing_client_visit: Mapped[float] = mapped_column("ExistingClientVisit", Numeric(34, 0), nullable=False)

class RegionaleKYCDetailORM(BaseOrm):
    __tablename__ = "BI_trd_Regional_eKYC_Details"

    region_name: Mapped[str] = mapped_column("region_Name", String(50), primary_key=True)
    cluster_name: Mapped[str] = mapped_column("cluster_Name", String(50))
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(50))
    total_investor: Mapped[float] = mapped_column("total_Investor", Numeric(34, 0), nullable=False)
    total_submitted: Mapped[float] = mapped_column("Total_Submitted", Numeric(34, 0), nullable=False)
    due: Mapped[float] = mapped_column("Due", Numeric(34, 0), nullable=False)

class RegionalEmployeeStructureORM(BaseOrm):
    __tablename__ = "BI_trd_Regional_Employee_stucture"

    region_name: Mapped[str] = mapped_column("region_name", String(50), primary_key=True)
    cluster_name: Mapped[str] = mapped_column("cluster_name", String(50))
    branch_code: Mapped[int] = mapped_column("branch_code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_name", String(50))
    permanent_trader: Mapped[float] = mapped_column("Permanent_trader", Numeric(34, 0), nullable=False)
    contractual_with_salary: Mapped[float] = mapped_column("Contractual_with_salary", Numeric(34, 0), nullable=False)
    contractual_without_salary: Mapped[float] = mapped_column("Contractual_without_salary", Numeric(34, 0), nullable=False)

class RegionalChannelWiseTradesORM(BaseOrm):
    __tablename__ = "BI_trd_Regional_ChannelWise_trades"

    region_name: Mapped[str] = mapped_column("region_Name", String(50), )
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer,primary_key=True) 
    branch_name: Mapped[str] = mapped_column("branch_Name", String(50))
    channel: Mapped[str] = mapped_column("channel", String(20),primary_key=True)
    total_clients: Mapped[int] = mapped_column("Total_Clients", Integer, nullable=False)
    total_trades: Mapped[int] = mapped_column("Trades", Integer, nullable=False)
    total_turnover: Mapped[float] = mapped_column("Total_Turnover", Numeric(34, 0), nullable=False)
    push_date: Mapped[datetime] = mapped_column("push_date", DateTime, nullable=False)


class RegionalPartyTurnoverCommissionORM(BaseOrm):
    __tablename__ = "BI_trd_Regional_Party_turnover_commission"

    region_name: Mapped[str] = mapped_column("region_name", String(50),)
    cluster_name: Mapped[str] = mapped_column("cluster_name", String(50),)
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer,primary_key=True) 
    branch_name: Mapped[str] = mapped_column("branch_Name", String(50))
    total_party: Mapped[int] = mapped_column("party_count", Integer, nullable=False)
    total_investor: Mapped[int] = mapped_column("investor_count", Integer, nullable=False)
    total_turnover: Mapped[float] = mapped_column("TurnOver", Numeric(34, 0), nullable=False)
    total_commission: Mapped[float] = mapped_column("commission", Numeric(34, 0), nullable=False)

class RegionalCashMarginDetailsORM(BaseOrm):
    __tablename__ = "BI_trd_Regional_Tpv_Cash_margin_dep_Witdrawal_details"

    region_name: Mapped[str] = mapped_column("region_Name", String(50),)
    branch_code: Mapped[int] = mapped_column("branch_Code", Integer,primary_key=True) 
    branch_name: Mapped[str] = mapped_column("branch_Name", String(50))
    total_deposit: Mapped[float] = mapped_column("Total_Deposit", Numeric(34, 0), nullable=False)
    total_withdrawal: Mapped[float] = mapped_column("Total_Withdrawal", Numeric(34, 0), nullable=False)
    total_portfolio: Mapped[float] = mapped_column("TPV", Numeric(34, 0), nullable=False)
    margin_negative: Mapped[float] = mapped_column("Margin_Negative", Numeric(34, 0), nullable=False)
    cash_available: Mapped[float] = mapped_column("Cash_Available", Numeric(34, 0), nullable=False)