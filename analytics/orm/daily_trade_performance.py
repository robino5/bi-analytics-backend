from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import mapped_column

from db import BaseOrm

__all__ = ["OverallSummaryOrm"]


class OverallSummaryOrm(BaseOrm):
    __tablename__ = "BI_trd_BranchWise_Client_Cash_Margin_Details"

    branch_code = mapped_column("branch_Code", Numeric(10), primary_key=True)
    branch_name = mapped_column("branch_Name", String(50))
    total_client = mapped_column("Total_client", Integer, nullable=False)
    total_active_client = mapped_column("Total_Active_client", Integer, nullable=False)
    cash_active_client = mapped_column("Cash_active_client", Integer, nullable=False)
    margin_active_client = mapped_column(
        "Margin_active_client", Integer, nullable=False
    )
    cash_balance = mapped_column("Cash_balance", Numeric(38, 4), nullable=True)
    cash_stock_balance = mapped_column(
        "Cash_Stock_balance", Numeric(38, 4), nullable=False
    )
    cash_daily_turnover = mapped_column(
        "Cash_Daily_TurnOver", Numeric(38, 4), nullable=False
    )
    margin_balance = mapped_column("Margin_balance", Numeric(38, 4), nullable=True)
    margin_stock_balance = mapped_column(
        "Margin_Stock_balance", Numeric(38, 4), nullable=False
    )
    margin_daily_turnover = mapped_column(
        "Margin_Daily_TurnOver", Numeric(38, 4), nullable=False
    )
    daily_turnover = mapped_column("Daily_TurnOver", Numeric(38, 6), nullable=False)
    net_buy_sell = mapped_column("Net_buy_sell", Numeric(38, 6), nullable=False)
