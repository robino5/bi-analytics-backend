from http import HTTPMethod  # noqa: I001


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, select
from core.renderer import CustomRenderer

from sqlalchemy.orm import Session

from authusers.models import User
from db import engine

from ..orm import ClusterManagerOrm, OverallSummaryOrm
from .utils import parse_summary

__all__ = ["get_basic_summaries", "get_basic_summaries_by_branchid"]


@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_basic_summaries(request: Request) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

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
        if current_user.is_cluster_manager():
            branches_qs = select(ClusterManagerOrm.branch_code).where(
                ClusterManagerOrm.manager_name == current_user.username
            )
            branch_codes = [result[0] for result in session.execute(branches_qs)]
            qs = qs.where(OverallSummaryOrm.branch_code.in_(branch_codes))
        if current_user.is_branch_manager() or current_user.is_regional_manager():
            qs = qs.where(
                OverallSummaryOrm.branch_code == current_user.profile.branch_id
            )

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
def get_basic_summaries_by_branchid(request: Request, id: int) -> Response:
    """fetch basic branch summary with branch_id"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

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

        if current_user.is_admin() or current_user.is_cluster_manager():
            qs = qs.where(OverallSummaryOrm.branch_code == id)
        else:
            qs = qs.where(
                OverallSummaryOrm.branch_code == current_user.profile.branch_id
            )

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
