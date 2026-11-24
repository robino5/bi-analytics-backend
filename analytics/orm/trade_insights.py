from db import BaseOrm
from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

__all__ = [
    "MarketSpotDataInvestorDrillDownORM",
    "MarketZGroupDataInvestorDrillDownORM",
    "MarketNegativeEquityHoldingScripAnalysisORM"
]


class MarketSpotDataInvestorDrillDownORM(BaseOrm):
    __tablename__ = "BI_trd_Market_Spot_data_Analysis_investor_Drilldown"

    symbol: Mapped[str] = mapped_column("company_S_Name", String(100), primary_key=True)
    investor_code: Mapped[str] = mapped_column("investor_code", String(20), primary_key=True)
    investor_name: Mapped[str] = mapped_column("f_name", String(100))
    account_type: Mapped[str] = mapped_column("acc_Type", String(50))
    current_balance: Mapped[float] = mapped_column("cur_balance", Numeric(34, 2))
    ledger_balance: Mapped[float] = mapped_column("ledger_balance", Numeric(34, 2))
    spot_buy_qty: Mapped[float] = mapped_column("Spot_buy_qty", Numeric(34, 2))
    spot_buy_amount: Mapped[float] = mapped_column("Spot_buy_amount", Numeric(34, 2))
    cash_deposit: Mapped[float] = mapped_column("cash_deposit", Numeric(34, 2))
    non_cash_deposit: Mapped[float] = mapped_column("Non_cash_deposit", Numeric(34, 2))
    used_excess_lbsl_fund: Mapped[float] = mapped_column("Used_Excess_Lbsl_fund", Numeric(34, 2))
    fund_using_level: Mapped[str] = mapped_column("FUND_USING_LEVEL", String(15))
    rm_branch: Mapped[str] = mapped_column("RM Branch", String(50))
    rm_name: Mapped[str] = mapped_column("RM Name", String(200))

class MarketZGroupDataInvestorDrillDownORM(BaseOrm):
    __tablename__ = "BI_trd_Market_Z_group_data_Analysis_investor_Drilldown"

    symbol: Mapped[str] = mapped_column("company_S_Name", String(100), primary_key=True)
    investor_code: Mapped[str] = mapped_column("investor_code", String(20), primary_key=True)
    investor_name: Mapped[str] = mapped_column("f_name", String(100))
    account_type: Mapped[str] = mapped_column("acc_Type", String(50))
    current_balance: Mapped[float] = mapped_column("cur_balance", Numeric(34, 2))
    ledger_balance: Mapped[float] = mapped_column("ledger_balance", Numeric(34, 2))
    z_buy_qty: Mapped[float] = mapped_column("Z_buy_qty", Numeric(34, 2))
    z_buy_amount: Mapped[float] = mapped_column("Z_buy_amount", Numeric(34, 2))
    cash_deposit: Mapped[float] = mapped_column("cash_deposit", Numeric(34, 2))
    non_cash_deposit: Mapped[float] = mapped_column("Non_cash_deposit", Numeric(34, 2))
    used_excess_lbsl_fund: Mapped[float] = mapped_column("Used_Excess_Lbsl_fund", Numeric(34, 2))
    fund_using_level: Mapped[str] = mapped_column("FUND_USING_LEVEL", String(15))
    rm_branch: Mapped[str] = mapped_column("RM Branch", String(50))
    rm_name: Mapped[str] = mapped_column("RM Name", String(200))

class MarketNegativeEquityHoldingScripAnalysisORM(BaseOrm):
    __tablename__ = "BI_trd_Market_NegativeEquity_Holding_Scrip_Analysis"

    company_name: Mapped[str] = mapped_column("company_F_Name", String(100))
    company_code: Mapped[str] = mapped_column("company_Code", String(100), primary_key=True)
    free_qty: Mapped[float] = mapped_column("free_qty", Numeric(34, 2))
    lock_qty: Mapped[float] = mapped_column("lock_qty", Numeric(34, 2))
    total_investor: Mapped[int] = mapped_column("total_investor", Integer)
    avg_price: Mapped[float] = mapped_column("avg_price", Numeric(34, 2))
    ltp: Mapped[str] = mapped_column("ltp", String(100))
    market_value: Mapped[float] = mapped_column("market_value", Numeric(34, 2))
    last_week_price: Mapped[float] = mapped_column("Last_week_price", Numeric(34, 2))

