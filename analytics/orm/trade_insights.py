from db import BaseOrm
from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

__all__ = [
    "MarketSpotDataInvestorDrillDownORM",

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
    

