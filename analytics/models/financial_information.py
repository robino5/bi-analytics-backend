from .base import BaseModel

__all__ = [
    "TotalDepositToday",
    "TotalDepositThisYear",
    "TotalWithdrawalToday",
    "TotalWithdrawalThisYear",
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

