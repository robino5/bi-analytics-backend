from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "ClientSegmentationSummaryOrm",
    "BranchWiseClientNumbersOrm",
    "NonPerformerClientOrm",
    "AdminBMClientSegmentationTurnoverOrm",
    "AdminBMClientSegmentationTPVOrm",
    "AdminBMClientSegmentationEquityOrm",
    "AdminBMClientSegmentationLedgerOrm",
    "AdminMarketShareOrm",
    "AdminGsecTurnoverOrm",
    "AdminGsecTurnoverComparisonOrm",
]


class ClientSegmentationSummaryOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_BM_client_segmentation_summary"
    customer_category: Mapped[str] = mapped_column(
        "Customer_Category", String(255), primary_key=True
    )
    total_clients: Mapped[int] = mapped_column("Total_Clients", Integer, default=0)


class BranchWiseClientNumbersOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_BM_client_branchWise"
    branch_name: Mapped[str] = mapped_column(
        "branch Name", String(255), primary_key=True
    )
    branch_code: Mapped[int] = mapped_column(
        "branch Code", Integer, nullable=False, primary_key=True
    )
    total_clients: Mapped[int] = mapped_column("Total client", Integer, default=0)
    total_client_percentage: Mapped[float] = mapped_column(
        "Branch (%)", Numeric(7, 4), default=0
    )


class NonPerformerClientOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_BM_Non_Performer_client"

    branch_name: Mapped[str] = mapped_column(
        "branch_Name", String(255), primary_key=True
    )
    branch_code: Mapped[int] = mapped_column(
        "branch_Code", Integer, nullable=False, primary_key=True
    )
    total_clients: Mapped[int] = mapped_column(
        "BranchWise_nonperformer", Integer, default=0
    )
    total_client_percentage: Mapped[float] = mapped_column(
        "Branch (%)", Numeric(7, 4), default=0
    )


class AdminBMClientSegmentationTurnoverOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_BM_client_segmentation_Turnover"

    customer_category: Mapped[str] = mapped_column(
        "Customer_Category", String(255), primary_key=True
    )
    turnover: Mapped[float] = mapped_column("Turnover", Numeric(34, 4), default=0)


class AdminBMClientSegmentationTPVOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_BM_client_segmentation_TPV"

    customer_category: Mapped[str] = mapped_column(
        "Customer_Category", String(255), primary_key=True
    )
    free_qty: Mapped[int] = mapped_column("Free_qty", Integer)
    lock_qty: Mapped[int] = mapped_column("Lock_qty", Integer)
    tpv_total: Mapped[float] = mapped_column("TPV_Total", Numeric(34, 4))
    tpv_free_qty_percentage: Mapped[float] = mapped_column(
        "TPV_FreeQty", Numeric(34, 4)
    )
    tpv_lock_qty_percentage: Mapped[float] = mapped_column(
        "TPV_LockQty", Numeric(34, 4)
    )


class AdminBMClientSegmentationEquityOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_BM_client_segmentation_Equity"

    customer_category: Mapped[str] = mapped_column(
        "Customer_Category", String(255), primary_key=True
    )
    equity: Mapped[float] = mapped_column("Equity", Numeric(34, 4), default=0)


class AdminBMClientSegmentationLedgerOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_BM_client_segmentation_Ledger"

    customer_category: Mapped[str] = mapped_column(
        "Customer_Category", String(255), primary_key=True
    )
    margin: Mapped[float] = mapped_column("Margin_Amount", Numeric(34, 4), default=0)


class AdminMarketShareOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_FT_Summary_data"

    year: Mapped[int] = mapped_column("year", Integer, primary_key=True)
    month: Mapped[str] = mapped_column("Month_year", String(100), primary_key=True)
    turnover_dse: Mapped[float] = mapped_column("DSE FTturnOver", Numeric(34, 2))
    turnover_lbsl: Mapped[float] = mapped_column("LBSL_FT_turnOver", Numeric(34, 2))
    trade_percentage: Mapped[float] = mapped_column("Percentage_Trade", Numeric(5, 2))

class AdminGsecTurnoverOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_GSEC_TurnOver_DateWise"

    turnover_gsec:Mapped[float]=mapped_column("turnover_gsec",Numeric(38,2))
    trading_date: Mapped[DateTime] = mapped_column("trading_date", DateTime,primary_key=True)

class AdminGsecTurnoverComparisonOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_GSEC_TurnOver_Comparison_YrWise"

    turnover:Mapped[float]=mapped_column("turnover",Numeric(38,2))
    turnover_gsec:Mapped[float]=mapped_column("turnover_gsec",Numeric(38,2))
    year: Mapped[float] = mapped_column("Year_sl", Numeric(10,0),primary_key=True)

