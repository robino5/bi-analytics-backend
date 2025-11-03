from typing import Optional
from .base import BaseModel

__all__ = [
    "TotalDepositToday",
    "TotalDepositThisYear",
    "TotalWithdrawalToday",
    "TotalWithdrawalThisYear",
    "TotalDepositMonthWise",
    "TotalPaymentMonthWise"
]

class TotalDepositToday(BaseModel):
    branch_code: int
    branch_name: str
    cash_deposit: float
    cheque_deposit: float
    scb_deposit: float
    pay_order: float
    cash_dividend: float
    ipo_mode: float


class TotalDepositThisYear(BaseModel):
    branch_code: int
    branch_name: str
    cash_deposit: float
    cheque_deposit: float
    scb_deposit: float
    pay_order: float
    cash_dividend: float
    ipo_mode: float

class TotalWithdrawalToday(BaseModel):
    branch_code: int
    branch_name: str
    cash_withdrawal: float
    cheque_withdrawal: float
    online_requisition: float
    rtsg: float
    pay_order: float
    cash_dividend_deduction: float
    ipo_mode: float


class TotalWithdrawalThisYear(BaseModel):
    branch_code: int
    branch_name: str
    cash_withdrawal: float
    cheque_withdrawal: float
    online_requisition: float
    rtsg: float
    pay_order: float
    cash_dividend_deduction: float
    ipo_mode: float

class TotalDepositMonthWise(BaseModel):
    branch_code: Optional[int] = None
    branch_name: Optional[str] = None
    january: float
    february: float
    march: float
    april: float
    may: float
    june: float
    july: float
    august: float
    september: float
    october: float
    november: float
    december: float

class TotalPaymentMonthWise(BaseModel):
    branch_code: int
    branch_name: str
    january: float
    february: float
    march: float
    april: float
    may: float
    june: float
    july: float
    august: float
    september: float
    october: float
    november: float
    december: float

