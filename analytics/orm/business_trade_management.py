from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = [
    "BoardTurnOverOrm",
    "BoardTurnOverBreakdownOrm",
    "MarketShareLBSLOrm",
    "ATBMarketShareSMEOrm",
    "CompanyWiseSaleableStockOrm",
    "InvestorWiseSaleableStockOrm",
    "CompanyWiseSaleableStockPercentageOrm"
]


class BoardTurnOverOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_BoardWise"
    push_date: Mapped[DateTime] = mapped_column(
        "push_date", DateTime, primary_key=True
    )
    board: Mapped[str] = mapped_column(
        "Board", String(255), nullable=False, primary_key=True
    )
    turnover: Mapped[float] = mapped_column("Turn Over (mn)", Numeric(34, 2), default=0)
    dse_percentage: Mapped[float] = mapped_column("DSE(%)", Numeric(34, 2), default=0)
    lbsl_turnover: Mapped[float] = mapped_column(
        "Lbsl Turn Over (mn)", Numeric(34, 2), default=0
    )
    lbsl_percentage: Mapped[float] = mapped_column("Lbsl(%)", Numeric(34, 2), default=0)


class BoardTurnOverBreakdownOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_MainBoardWise_breakdown"
    push_date: Mapped[DateTime] = mapped_column(
        "push_date", DateTime, primary_key=True
    )
    board: Mapped[str] = mapped_column(
        "Main Board", String(255), nullable=False, primary_key=True
    )
    turnover: Mapped[float] = mapped_column("Turn Over (mn)", Numeric(34, 2), default=0)
    dse_percentage: Mapped[float] = mapped_column("DSE(%)", Numeric(34, 2), default=0)
    lbsl_turnover: Mapped[float] = mapped_column(
        "Lbsl Turn Over (mn)", Numeric(34, 2), default=0
    )
    lbsl_percentage: Mapped[float] = mapped_column("Lbsl(%)", Numeric(34, 2), default=0)


class MarketShareLBSLOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_details_market_share_LBSL"

    trading_date: Mapped[DateTime] = mapped_column("trd_dt", DateTime, primary_key=True)
    lbsl_buy_of_dse: Mapped[float] = mapped_column("LBSL BUY of DSE", Numeric(34, 2))
    lbsl_sale_of_dse: Mapped[float] = mapped_column("LBSL SALE of DSE", Numeric(34, 2))
    lbsl_total_of_dse: Mapped[float] = mapped_column(
        "LBSL Total of DSE", Numeric(34, 2)
    )
    dse_market_turnover: Mapped[float] = mapped_column(
        "DSE Market Turnover", Numeric(34, 2)
    )
    lbsl_share_of_dse: Mapped[float] = mapped_column(
        "LBSL Share of DSE", Numeric(34, 2)
    )
    lbsl_buy_of_cse: Mapped[float] = mapped_column("LBSL BUY of CSE", Numeric(34, 2))
    lbsl_sale_of_cse: Mapped[float] = mapped_column("LBSL SALE of CSE", Numeric(34, 2))
    lbsl_total_of_cse: Mapped[float] = mapped_column(
        "LBSL Total of CSE", Numeric(34, 2)
    )
    cse_market_turnover: Mapped[float] = mapped_column(
        "CSE Market Turnover", Numeric(34, 2)
    )
    lbsl_share_of_cse: Mapped[float] = mapped_column(
        "LBSL Share of CSE", Numeric(34, 2)
    )
    lbsl_total_turnover: Mapped[float] = mapped_column(
        "LBSL Total Turnover", Numeric(34, 2)
    )
    exch_total_market: Mapped[float] = mapped_column(
        "EXCH Total Market TO", Numeric(34, 2)
    )
    lbsl_market_all: Mapped[float] = mapped_column(
        "LBSL Market % (DSE+CSE)", Numeric(34, 2)
    )
    foreign: Mapped[float] = mapped_column("Foreign", Numeric(34, 2), default=0)
    net_income: Mapped[float] = mapped_column("Net Income", Numeric(34, 2))


class ATBMarketShareSMEOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_details_SME_ATB_market_share_LBSL"

    trading_date: Mapped[DateTime] = mapped_column("trd_dt", DateTime, primary_key=True)
    dse_sme_turnover: Mapped[float] = mapped_column(
        "LBSL DSE SME TurnOver", Numeric(34, 2)
    )
    dse_atb_turnover: Mapped[float] = mapped_column(
        "LBSL DSE ATB Turnover", Numeric(34, 2)
    )
    dse_gsec_turnover: Mapped[float] = mapped_column(
        "LBSL DSE GSEC Turnover", Numeric(34, 2)
    )
    dse_block_turnover: Mapped[float] = mapped_column(
        "LBSL DSE Block Turnover", Numeric(34, 2)
    )
    sme_percent: Mapped[float] = mapped_column("LBSL SME (%)", Numeric(34, 2))
    atb_percent: Mapped[float] = mapped_column("LBSL ATB (%)", Numeric(34, 2))
    cse_sme_turnover: Mapped[float] = mapped_column(
        "LBSL CSE SME TurnOver", Numeric(34, 2)
    )
    cse_atb_turnover: Mapped[float] = mapped_column(
        "LBSL CSE ATB Turnover", Numeric(34, 2)
    )
    cse_gsec_turnover: Mapped[float] = mapped_column(
        "LBSL CSE GSEC Turnover", Numeric(34, 2)
    )
    cse_block_turnover: Mapped[float] = mapped_column(
        "LBSL CSE Block Turnover", Numeric(34, 2)
    )
    cse_sme_percent: Mapped[float] = mapped_column("LBSL CSE SME (%)", Numeric(34, 2))
    cse_atb_percent: Mapped[float] = mapped_column("LBSL CSE ATB (%)", Numeric(34, 2))


class CompanyWiseSaleableStockOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_CompanyWise_Total_saleable_Stock"

    company_name: Mapped[str] = mapped_column(
        "company_F_Name", String(255), primary_key=True
    )
    stock_available: Mapped[int] = mapped_column("Total_Stock", Integer)
    gsec_flag: Mapped[int] = mapped_column("GSEC_Flag", Integer)


class InvestorWiseSaleableStockOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_Client_saleable_Stock"

    company_name: Mapped[str] = mapped_column(
        "company Name", String(255), primary_key=True
    )
    branch_name: Mapped[str] = mapped_column("Client branch", String(255))
    investor_code: Mapped[str] = mapped_column(
        "investor code", String(255), primary_key=True
    )
    client_name: Mapped[str] = mapped_column("Client Name", String(255))
    rm_name: Mapped[str] = mapped_column("RM", String(255))
    stock_available: Mapped[int] = mapped_column("Total saleable Stock", Integer)


class CompanyWiseSaleableStockPercentageOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_Client_saleable_Stock_percentages"

    company_name: Mapped[str] = mapped_column(
        "company_F_Name", String(255), primary_key=True
    )
    branch_name: Mapped[str] = mapped_column("Branch_name", String(255), primary_key=True)
    stock_available: Mapped[int] = mapped_column("Total_Stock", Integer)
    stock_available_percentage: Mapped[float] = mapped_column("Stock_percentage", Numeric(6,4))



    
