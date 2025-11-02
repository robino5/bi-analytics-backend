
from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm
__all__ = [
    "TotalDepositTodayOrm", 
    "TotalDepositThisYearOrm",
    "TotalWithdrawalTodayOrm",
    "TotalWithdrawalThisYearOrm",
]

class TotalDepositTodayOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_Fin_branchWise_Collection"

    branch_code: Mapped[int] = mapped_column("Branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("Branch_name", String(255), nullable=False)
    cash_deposit: Mapped[float] = mapped_column("Cash_deposit", Numeric(34, 2))
    cheque_deposit: Mapped[float] = mapped_column("Cheque_deposit", Numeric(34, 2))
    scb_deposit: Mapped[float] = mapped_column("Scb_deposit", Numeric(34, 2))
    pay_order: Mapped[float] = mapped_column("Pay_order", Numeric(34, 2))
    cash_dividend: Mapped[float] = mapped_column("Cash_dividend", Numeric(34, 2))
    ipo_mode: Mapped[float] = mapped_column("IPO_Mode", Numeric(34, 2))


class TotalDepositThisYearOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_Fin_branchWise_Collection_hist"
  
    branch_code: Mapped[int] = mapped_column("Branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("Branch_name", String(255), nullable=False)
    cash_deposit: Mapped[float] = mapped_column("Cash_deposit", Numeric(34, 2))
    cheque_deposit: Mapped[float] = mapped_column("Cheque_deposit", Numeric(34, 2))
    scb_deposit: Mapped[float] = mapped_column("Scb_deposit", Numeric(34, 2))
    pay_order: Mapped[float] = mapped_column("Pay_order", Numeric(34, 2))
    cash_dividend: Mapped[float] = mapped_column("Cash_dividend", Numeric(34, 2))
    ipo_mode: Mapped[float] = mapped_column("IPO_Mode", Numeric(34, 2))

class TotalWithdrawalTodayOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_Fin_branchWise_payment"

    branch_code: Mapped[int] = mapped_column("Branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("Branch_name", String(255), nullable=False)
    cash_withdrawal: Mapped[float] = mapped_column("Cash_Witdrawal", Numeric(34, 2))
    cheque_withdrawal: Mapped[float] = mapped_column("Cheque_Witdrawal", Numeric(34, 2))
    online_requisition: Mapped[float] = mapped_column("Online_Requisition", Numeric(34, 2))
    rtsg: Mapped[float] = mapped_column("RTGS", Numeric(34, 2))
    pay_order: Mapped[float] = mapped_column("Pay_order", Numeric(34, 2))
    cash_dividend_deduction: Mapped[float] = mapped_column("Cash_dividend_deduction", Numeric(34, 2))
    ipo_mode: Mapped[float] = mapped_column("IPO_Mode", Numeric(34, 2))


class TotalWithdrawalThisYearOrm(BaseOrm):
    __tablename__ = "BI_trd_Admin_Fin_branchWise_payment_hist"

    branch_code: Mapped[int] = mapped_column("Branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("Branch_name", String(255), nullable=False)
    cash_withdrawal: Mapped[float] = mapped_column("Cash_Witdrawal", Numeric(34, 2))
    cheque_withdrawal: Mapped[float] = mapped_column("Cheque_Witdrawal", Numeric(34, 2))
    online_requisition: Mapped[float] = mapped_column("Online_Requisition", Numeric(34, 2))
    rtsg: Mapped[float] = mapped_column("RTGS", Numeric(34, 2))
    pay_order: Mapped[float] = mapped_column("Pay_order", Numeric(34, 2))
    cash_dividend_deduction: Mapped[float] = mapped_column("Cash_dividend_deduction", Numeric(34, 2))
    ipo_mode: Mapped[float] = mapped_column("IPO_Mode", Numeric(34, 2))

