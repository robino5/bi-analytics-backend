from http import HTTPMethod
from typing import Any, Dict
from datetime import datetime
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import Sequence, func, select
from sqlalchemy.orm import Session
from drf_spectacular.utils import OpenApiParameter, extend_schema

from core.metadata.openapi import OpenApiTags
from core.permissions import IsManagementUser
from core.renderer import CustomRenderer
from db import engine

from ..models import (
    TotalDepositToday,
    TotalDepositThisYear,
    TotalWithdrawalToday,
    TotalWithdrawalThisYear,
    TotalDepositMonthWise,
    TotalPaymentMonthWise
)
from ..orm import (
    TotalDepositTodayOrm,
    TotalDepositThisYearOrm,
    TotalWithdrawalTodayOrm,
    TotalWithdrawalThisYearOrm,
    TotalDepositMonthWiseORM,
    TotalPaymentMonthWiseORM
)

__all__ = [
    "get_admin_total_deposit_branch_wise_today",
    "get_admin_total_deposit_branch_wise_this_year",
    "get_admin_total_withdrawal_branch_wise_today",
    "get_admin_total_withdrawal_branch_wise_this_year",
    "get_admin_total_deposit_branch_wise_monthly",
    "get_admin_total_withdrawal_branch_wise_monthly"
]


def get_sum_of_property(property: str, rows: Sequence[Dict[str, Any]]) -> int:
    sum = 0
    for row in rows:
        sum += row.get(property, 0)
    return round(sum)

#### Total Deposit Today ####
@extend_schema(tags=[OpenApiTags.FINANCIAL_INFORMATION])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_total_deposit_branch_wise_today(request: Request) -> Response:
    """fetch admin total deposit branch wise today"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TotalDepositTodayOrm).order_by(
                TotalDepositTodayOrm.branch_code
            )
        ).scalars()

        results = [TotalDepositToday.model_validate(row).model_dump() for row in qs]

        
    response = {
        "detail": {
            "total_deposit": get_sum_of_property("cash_deposit", results)
            +get_sum_of_property("cheque_deposit", results)
            +get_sum_of_property("scb_deposit", results)
            +get_sum_of_property("pay_order", results)
            +get_sum_of_property("cash_dividend", results)
            +get_sum_of_property("ipo_mode", results),
           "cash_deposit": get_sum_of_property("cash_deposit", results),
           "cheque_deposit": get_sum_of_property("cheque_deposit", results),
           "scb_deposit": get_sum_of_property("scb_deposit", results),
           "pay_order": get_sum_of_property("pay_order", results),
           "cash_dividend": get_sum_of_property("cash_dividend", results),
           "ipo_mode": get_sum_of_property("ipo_mode", results),
        },
        "rows": results,
    }

    return Response(response)

#### Total Deposit This Year ####
@extend_schema(tags=[OpenApiTags.FINANCIAL_INFORMATION])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_total_deposit_branch_wise_this_year(request: Request) -> Response:
    """fetch admin total deposit branch wise this year"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TotalDepositThisYearOrm).order_by(
                TotalDepositThisYearOrm.branch_code
            )
        ).scalars()

        results = [TotalDepositThisYear.model_validate(row).model_dump() for row in qs]

        
    response = {
        "detail": {
            "total_deposit": get_sum_of_property("cash_deposit", results)
            +get_sum_of_property("cheque_deposit", results)
            +get_sum_of_property("scb_deposit", results)
            +get_sum_of_property("pay_order", results)
            +get_sum_of_property("cash_dividend", results)
            +get_sum_of_property("ipo_mode", results),
            "cash_deposit": get_sum_of_property("cash_deposit", results),
            "cheque_deposit": get_sum_of_property("cheque_deposit", results),
            "scb_deposit": get_sum_of_property("scb_deposit", results),
            "pay_order": get_sum_of_property("pay_order", results),
            "cash_dividend": get_sum_of_property("cash_dividend", results),
            "ipo_mode": get_sum_of_property("ipo_mode", results),
        },
        "rows": results,
    }

    return Response(response)

#### Total Withdrawal Today ####
@extend_schema(tags=[OpenApiTags.FINANCIAL_INFORMATION])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_total_withdrawal_branch_wise_today(request: Request) -> Response:
    """fetch admin total withdrawal branch wise today"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TotalWithdrawalTodayOrm).order_by(
                TotalWithdrawalTodayOrm.branch_code
            )
        ).scalars()

        results = [TotalWithdrawalToday.model_validate(row).model_dump() for row in qs]

        
    response = {
        "detail": {
            "total_withdrawal": get_sum_of_property("cash_withdrawal", results)
            +get_sum_of_property("cheque_withdrawal", results)
            +get_sum_of_property("online_requisition", results)
            +get_sum_of_property("rtgs", results)
            +get_sum_of_property("cash_dividend_deduction", results)
            +get_sum_of_property("pay_order", results)
            +get_sum_of_property("ipo_mode", results),
            "cash_withdrawal": get_sum_of_property("cash_withdrawal", results),
            "cheque_withdrawal": get_sum_of_property("cheque_withdrawal", results),
            "online_requisition": get_sum_of_property("online_requisition", results),
            "rtgs": get_sum_of_property("rtgs", results),
            "cash_dividend_deduction": get_sum_of_property("cash_dividend_deduction", results),
            "pay_order": get_sum_of_property("pay_order", results),
            "ipo_mode": get_sum_of_property("ipo_mode", results),
        },
        "rows": results,
    }

    return Response(response)


#### Total Withdrawal This Year ####
@extend_schema(tags=[OpenApiTags.FINANCIAL_INFORMATION])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_total_withdrawal_branch_wise_this_year(request: Request) -> Response:
    """fetch admin total withdrawal branch wise this year"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TotalWithdrawalThisYearOrm).order_by(
                TotalWithdrawalThisYearOrm.branch_code
            )
        ).scalars()

        results = [TotalWithdrawalThisYear.model_validate(row).model_dump() for row in qs]

        
    response = {
        "detail": {
            "total_withdrawal": get_sum_of_property("cash_withdrawal", results)
            +get_sum_of_property("cheque_withdrawal", results)
            +get_sum_of_property("online_requisition", results)
            +get_sum_of_property("rtgs", results)
            +get_sum_of_property("cash_dividend_deduction", results)
            +get_sum_of_property("pay_order", results)
            +get_sum_of_property("ipo_mode", results),
            "cash_withdrawal": get_sum_of_property("cash_withdrawal", results),
            "cheque_withdrawal": get_sum_of_property("cheque_withdrawal", results),
            "online_requisition": get_sum_of_property("online_requisition", results),
            "rtgs": get_sum_of_property("rtgs", results),
            "cash_dividend_deduction": get_sum_of_property("cash_dividend_deduction", results),
            "pay_order": get_sum_of_property("pay_order", results),
            "ipo_mode": get_sum_of_property("ipo_mode", results),
        },
        "rows": results,
    }

    return Response(response)


#### Total Deposit Month Wise  ####
@extend_schema(tags=[OpenApiTags.FINANCIAL_INFORMATION])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_total_deposit_branch_wise_monthly(request: Request) -> Response:
    """fetch admin total deposit branch wise monthly"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TotalDepositMonthWiseORM).order_by(
                TotalDepositMonthWiseORM.branch_code
            )
        ).scalars()

        results = [TotalDepositMonthWise.model_validate(row).model_dump() for row in qs]

        response = {
        "monthly_wise": {
           "january": get_sum_of_property("january", results),
           "february": get_sum_of_property("february", results),
            "march": get_sum_of_property("march", results),
            "april": get_sum_of_property("april", results),
            "may": get_sum_of_property("may", results),
            "june": get_sum_of_property("june", results),
            "july": get_sum_of_property("july", results),
            "august": get_sum_of_property("august", results),
            "september": get_sum_of_property("september", results),
            "october": get_sum_of_property("october", results),
            "november": get_sum_of_property("november", results),
            "december": get_sum_of_property("december", results),
        },
        "rows": results,
    }


    return Response(response)


#### Total Withdrawal Month Wise  ####
@extend_schema(tags=[OpenApiTags.FINANCIAL_INFORMATION])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_total_withdrawal_branch_wise_monthly(request: Request) -> Response:
    """fetch admin total withdrawal branch wise monthly"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TotalPaymentMonthWiseORM).order_by(
                TotalPaymentMonthWiseORM.branch_code
            )
        ).scalars()

        results = [TotalPaymentMonthWise.model_validate(row).model_dump() for row in qs]

        response = {
        "monthly_wise": {
           "january": get_sum_of_property("january", results),
           "february": get_sum_of_property("february", results),
            "march": get_sum_of_property("march", results),
            "april": get_sum_of_property("april", results),
            "may": get_sum_of_property("may", results),
            "june": get_sum_of_property("june", results),
            "july": get_sum_of_property("july", results),
            "august": get_sum_of_property("august", results),
            "september": get_sum_of_property("september", results),
            "october": get_sum_of_property("october", results),
            "november": get_sum_of_property("november", results),
            "december": get_sum_of_property("december", results),
        },
        "rows": results,
    }


    return Response(response)




