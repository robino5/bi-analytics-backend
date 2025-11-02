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
    TotalWithdrawalThisYear
)
from ..orm import (
    TotalDepositTodayOrm,
    TotalDepositThisYearOrm,
    TotalWithdrawalTodayOrm,
    TotalWithdrawalThisYearOrm
)

__all__ = [
    "get_admin_total_deposit_branch_wise_today",
    "get_admin_total_deposit_branch_wise_this_year",
    "get_admin_total_withdrawal_branch_wise_today",
    "get_admin_total_withdrawal_branch_wise_this_year",
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
            "total_deposit_today": get_sum_of_property("cash_deposit", results)
            +get_sum_of_property("cheque_deposit", results)
            +get_sum_of_property("scb_deposit", results)
            +get_sum_of_property("pay_order", results)
            +get_sum_of_property("cash_dividend", results)
            +get_sum_of_property("ipo_mode", results),
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
            "total_deposit_today": get_sum_of_property("cash_deposit", results)
            +get_sum_of_property("cheque_deposit", results)
            +get_sum_of_property("scb_deposit", results)
            +get_sum_of_property("pay_order", results)
            +get_sum_of_property("cash_dividend", results)
            +get_sum_of_property("ipo_mode", results),
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
            "total_withdrawal_today": get_sum_of_property("cash_withdrawal", results)
            +get_sum_of_property("cheque_withdrawal", results)
            +get_sum_of_property("online_requisition", results)
            +get_sum_of_property("rtsg", results)
            +get_sum_of_property("cash_dividend_deduction", results)
            +get_sum_of_property("pay_order", results)
            +get_sum_of_property("ipo_mode", results)
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
            "total_withdrawal_this_year": get_sum_of_property("cash_withdrawal", results)
            +get_sum_of_property("cheque_withdrawal", results)
            +get_sum_of_property("online_requisition", results)
            +get_sum_of_property("rtsg", results)
            +get_sum_of_property("cash_dividend_deduction", results)
            +get_sum_of_property("pay_order", results)
            +get_sum_of_property("ipo_mode", results)
        },
        "rows": results,
    }

    return Response(response)


