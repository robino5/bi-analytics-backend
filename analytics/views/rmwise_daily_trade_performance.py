from http import HTTPMethod

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import desc, func, select, text
from sqlalchemy.orm import Session

from authusers.models import User
from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer
from db import engine

from ..models import DailyTurnoverPerformance, SectorExposure
from ..orm import (
    RMWiseDailyTurnoverPerformanceOrm,
    RMWiseOverallSummaryOrm,
    RMWiseSectorExposureCashCodeOrm,
    RMWiseSectorExposureMarginCodeOrm,
)
from .utils import inject_branchwise_filter, parse_summary

__all__ = [
    "get_basic_summaries_rmwise",
    "get_turnover_performance_statistics_rmwise",
    "get_cashcode_sector_exposure_rmwise",
    "get_margincode_sector_exposure_rmwise",
]

SUMMARY_QUERY_STR = select(
    func.sum(RMWiseOverallSummaryOrm.total_client).label("total_clients"),
    func.sum(RMWiseOverallSummaryOrm.total_active_client).label("total_active_clients"),
    func.sum(RMWiseOverallSummaryOrm.cash_active_client).label("cash_active_clients"),
    func.sum(RMWiseOverallSummaryOrm.cash_balance).label("cash_balance"),
    func.sum(RMWiseOverallSummaryOrm.cash_stock_balance).label("cash_stock_balance"),
    func.sum(RMWiseOverallSummaryOrm.cash_daily_turnover).label("cash_daily_turnover"),
    func.sum(RMWiseOverallSummaryOrm.margin_stock_balance).label(
        "margin_stock_balance"
    ),
    func.sum(RMWiseOverallSummaryOrm.margin_balance).label("margin_balance"),
    func.sum(RMWiseOverallSummaryOrm.margin_active_client).label(
        "margin_active_clients"
    ),
    func.sum(RMWiseOverallSummaryOrm.margin_daily_turnover).label(
        "margin_daily_turnover"
    ),
    func.sum(RMWiseOverallSummaryOrm.daily_turnover).label("daily_turnover"),
    func.sum(RMWiseOverallSummaryOrm.net_buy_sell).label("net_buy_sell"),
)

METRICS_OF_SUMMARY_QUERY = {
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


@extend_schema(
    tags=[OpenApiTags.RMWISE_DTP],
    parameters=[
        OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=True,
            description="Branch Code Of the RM",
        ),
        OpenApiParameter(
            "username",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Username of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_basic_summaries_rmwise(request: Request) -> Response:
    """fetch basic branch summary rmwise data"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    branch_query = request.query_params.get("branch_code", None)
    rm_id = request.query_params.get("username", None)

    with Session(engine) as session:
        qs = SUMMARY_QUERY_STR
        qs = inject_branchwise_filter(qs, current_user, RMWiseOverallSummaryOrm)

        if branch_query:
            qs = qs.where(
                RMWiseOverallSummaryOrm.branch_code == branch_query,
            )
        if rm_id:
            qs = qs.where(
                RMWiseOverallSummaryOrm.rm_id == rm_id,
            )

        rows = session.execute(qs).first()._asdict()

        results = {
            key: {"name": METRICS_OF_SUMMARY_QUERY[key], "value": value}
            for key, value in rows.items()
            if key in METRICS_OF_SUMMARY_QUERY
        }

        short_summary = parse_summary(results, "short_summary")
        cash_code_summary = parse_summary(results, "cash_code_summary")
        margin_code_summary = parse_summary(results, "margin_code_summary")

        merged_dict = short_summary | cash_code_summary | margin_code_summary
    return Response(merged_dict)


@extend_schema(
    tags=[OpenApiTags.RMWISE_DTP],
    parameters=[
        OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=True,
            description="Branch Code Of the RM",
        ),
        OpenApiParameter(
            "username",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Username of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_turnover_performance_statistics_rmwise(request: Request) -> Response:
    """fetch the turnover performance statistics rm wise"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    branch_query = request.query_params.get("branch_code", None)
    rm_id = request.query_params.get("username", None)

    with Session(engine) as session:
        qs = (
            select(
                RMWiseDailyTurnoverPerformanceOrm.trading_date.label("label"),
                func.sum(RMWiseDailyTurnoverPerformanceOrm.generated).label(
                    "generated"
                ),
                func.sum(RMWiseDailyTurnoverPerformanceOrm.target).label("target"),
            )
            .group_by(RMWiseDailyTurnoverPerformanceOrm.trading_date)
            .order_by(RMWiseDailyTurnoverPerformanceOrm.trading_date)
        )
        qs = inject_branchwise_filter(
            qs, current_user, RMWiseDailyTurnoverPerformanceOrm
        )

        if branch_query:
            qs = qs.where(
                RMWiseDailyTurnoverPerformanceOrm.branch_code == branch_query,
            )
        if rm_id:
            qs = qs.where(
                RMWiseDailyTurnoverPerformanceOrm.rm_id == rm_id,
            )
        rows = session.execute(qs)

        results = [
            DailyTurnoverPerformance.model_validate(row).model_dump() for row in rows
        ]

    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RMWISE_DTP],
    parameters=[
        OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=True,
            description="Branch Code Of the RM",
        ),
        OpenApiParameter(
            "username",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Username of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_cashcode_sector_exposure_rmwise(request: Request) -> Response:
    """fetch the margin loan statistics for all"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    branch_query = request.query_params.get("branch_code", None)
    rm_id = request.query_params.get("username", None)

    with Session(engine) as session:
        qs = (
            select(
                RMWiseSectorExposureCashCodeOrm.sector_name.label("name"),
                func.sum(RMWiseSectorExposureCashCodeOrm.total_qty).label("value"),
            )
            .group_by(RMWiseSectorExposureCashCodeOrm.sector_name)
            .order_by(desc(text("value")))
        )

        qs = inject_branchwise_filter(qs, current_user, RMWiseSectorExposureCashCodeOrm)

        if branch_query:
            qs = qs.where(
                RMWiseDailyTurnoverPerformanceOrm.branch_code == branch_query,
            )
        if rm_id:
            qs = qs.where(
                RMWiseDailyTurnoverPerformanceOrm.rm_id == rm_id,
            )
        rows = session.execute(qs)

        results = [SectorExposure.model_validate(row).model_dump() for row in rows]

    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RMWISE_DTP],
    parameters=[
        OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=True,
            description="Branch Code Of the RM",
        ),
        OpenApiParameter(
            "username",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Username of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margincode_sector_exposure_rmwise(request: Request) -> Response:
    """fetch the margin loan statistics for all"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    branch_query = request.query_params.get("branch_code", None)
    rm_id = request.query_params.get("username", None)

    with Session(engine) as session:
        qs = (
            select(
                RMWiseSectorExposureMarginCodeOrm.sector_name.label("name"),
                func.sum(RMWiseSectorExposureMarginCodeOrm.total_qty).label("value"),
            )
            .group_by(RMWiseSectorExposureMarginCodeOrm.sector_name)
            .order_by(desc(text("value")))
        )

        qs = inject_branchwise_filter(
            qs, current_user, RMWiseSectorExposureMarginCodeOrm
        )

        if branch_query:
            qs = qs.where(
                RMWiseDailyTurnoverPerformanceOrm.branch_code == branch_query,
            )
        if rm_id:
            qs = qs.where(
                RMWiseDailyTurnoverPerformanceOrm.rm_id == rm_id,
            )
        rows = session.execute(qs)

        results = [SectorExposure.model_validate(row).model_dump() for row in rows]

    return Response(results)
