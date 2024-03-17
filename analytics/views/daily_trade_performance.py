from http import HTTPMethod  # noqa: I001


from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, select
from core.renderer import CustomRenderer
from core.constants import DEFAULT_CACHE_TIME

from sqlalchemy.orm import Session

from authusers.models import User
from db import engine

from ..orm import ClusterManagerOrm, OverallSummaryOrm
from .utils import parse_summary

from devtools import debug  # noqa: I401


__all__ = ["get_basic_summaries", "get_basic_summaries_by_branchid"]


@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
@cache_page(DEFAULT_CACHE_TIME)
def get_basic_summaries(request: Request) -> Response:
    request.accepted_renderer = CustomRenderer()

    """fetch basic branch summary"""
    current_user: User = request.user
    debug(current_user)
    with Session(engine) as session:
        qs = select(
            func.sum(OverallSummaryOrm.total_client).label("total_clients"),
            func.sum(OverallSummaryOrm.total_active_client).label(
                "total_active_clients"
            ),
            func.sum(OverallSummaryOrm.cash_active_client).label("cash_active_clients"),
            func.sum(OverallSummaryOrm.cash_balance).label("cash_balance"),
            func.sum(OverallSummaryOrm.cash_stock_balance).label("cash_stock_balance"),
            func.sum(OverallSummaryOrm.cash_daily_turnover).label(
                "cash_daily_turnover"
            ),
            func.sum(OverallSummaryOrm.margin_stock_balance).label(
                "margin_stock_balance"
            ),
            func.sum(OverallSummaryOrm.margin_balance).label("margin_balance"),
            func.sum(OverallSummaryOrm.margin_active_client).label(
                "margin_active_clients"
            ),
            func.sum(OverallSummaryOrm.margin_daily_turnover).label(
                "margin_daily_turnover"
            ),
            func.sum(OverallSummaryOrm.daily_turnover).label("daily_turnover"),
            func.sum(OverallSummaryOrm.net_buy_sell).label("net_buy_sell"),
        )
        if not current_user.is_admin():
            branches_qs = select(ClusterManagerOrm.branch_code).where(
                ClusterManagerOrm.manager_name == current_user.username
            )
            branch_codes = [result[0] for result in session.execute(branches_qs)]
            qs = qs.where(OverallSummaryOrm.branch_code.in_(branch_codes))

        rows = session.execute(qs).first()._asdict()

        metric_names = {
            "total_clients": "Total Client",
            "total_active_clients": "Active Clients",
            "daily_turnover": "TurnOver",
            "net_buy_sell": "Net Buy/Sell",
            "cash_balance": "Cash Balance",
            "cash_active_clients": "Active Clients",
            "cash_stock_balance": "Stock Balance",
            "cash_daily_turnover": "TurnOver",
            "margin_stock_balance": "Stock Balance",
            "margin_active_clients": "Active Clients",
            "margin_daily_turnover": "TurnOver",
            "margin_balance": "Loan Balance",
        }

        results = {
            key: {"name": metric_names[key], "value": value}
            for key, value in rows.items()
            if key in metric_names
        }

        short_summary = parse_summary(results, "short_summary")
        cash_code_summary = parse_summary(results, "cash_code_summary")
        margin_code_summary = parse_summary(results, "margin_code_summary")

        merged_dict = short_summary | cash_code_summary | margin_code_summary
    return Response(merged_dict)


@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_basic_summaries_by_branchid(request: Request, branch_id: int) -> Response:
    request.accepted_renderer = CustomRenderer()

    """fetch basic branch summary"""
    current_user: User = request.user
    return Response({"user": current_user.__dict__, "branch_id": branch_id})
