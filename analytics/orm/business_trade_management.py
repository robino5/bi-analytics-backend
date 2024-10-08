from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = ["BoardTurnOverOrm", "BoardTurnOverBreakdownOrm"]


class BoardTurnOverOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_RealTime_Turnover_BoardWise"
    trading_date: Mapped[DateTime] = mapped_column(
        "trading_Date", DateTime, primary_key=True
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
    trading_date: Mapped[DateTime] = mapped_column(
        "trading_Date", DateTime, primary_key=True
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
