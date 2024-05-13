from datetime import datetime, timedelta
from http import HTTPMethod

from drf_spectacular.utils import extend_schema
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

from ..models import DailyMarginLoanUsage, DailyTurnoverPerformance, SectorExposure
from ..orm import (
    DailyMarginLoanUsageOrm,
    DailyTurnoverPerformanceOrm,
    OverallSummaryOrm,
    SectorExposureCashCodeOrm,
    SectorExposureMarginCodeOrm,
)
from .utils import parse_summary, rolewise_branch_data_filter

__all__ = [
    "get_basic_summaries",
    "get_basic_summaries_by_branchid",
    "get_turnover_performance_statistics",
    "get_turnover_performance_statistics_by_branchid",
    "get_margin_loan_statistics",
    "get_margin_loan_statistics_by_branchid",
    "get_cashcode_sector_exposure",
    "get_margincode_sector_exposure",
    "get_cashcode_sector_exposure_by_branchid",
    "get_margincode_sector_exposure_by_branchid",
]

SUMMARY_QUERY_STR = select(
    func.sum(OverallSummaryOrm.total_client).label("total_clients"),
    func.sum(OverallSummaryOrm.total_active_client).label("total_active_clients"),
    func.sum(OverallSummaryOrm.cash_active_client).label("cash_active_clients"),
    func.sum(OverallSummaryOrm.cash_balance).label("cash_balance"),
    func.sum(OverallSummaryOrm.cash_stock_balance).label("cash_stock_balance"),
    func.sum(OverallSummaryOrm.cash_daily_turnover).label("cash_daily_turnover"),
    func.sum(OverallSummaryOrm.margin_stock_balance).label("margin_stock_balance"),
    func.sum(OverallSummaryOrm.margin_balance).label("margin_balance"),
    func.sum(OverallSummaryOrm.margin_active_client).label("margin_active_clients"),
    func.sum(OverallSummaryOrm.margin_daily_turnover).label("margin_daily_turnover"),
    func.sum(OverallSummaryOrm.daily_turnover).label("daily_turnover"),
    func.sum(OverallSummaryOrm.net_buy_sell).label("net_buy_sell"),
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


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_basic_summaries(request: Request) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = SUMMARY_QUERY_STR
        qs = rolewise_branch_data_filter(qs, current_user, OverallSummaryOrm)

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


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_basic_summaries_by_branchid(request: Request, id: int) -> Response:
    """fetch basic branch summary with branch_id"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = SUMMARY_QUERY_STR
        if current_user.is_admin() or current_user.is_cluster_manager():
            qs = qs.where(OverallSummaryOrm.branch_code == id)
        else:
            qs = qs.where(
                OverallSummaryOrm.branch_code == current_user.profile.branch_id
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


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_turnover_performance_statistics(request: Request) -> Response:
    """fetch the turnover performance statistics for all"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    # defining a threshold-date as sometimes database returning very old data
    threshold_date = datetime.now() - timedelta(days=120)

    with Session(engine) as session:
        qs = (
            select(
                DailyTurnoverPerformanceOrm.trading_date.label("label"),
                func.sum(DailyTurnoverPerformanceOrm.generated).label("generated"),
                func.sum(DailyTurnoverPerformanceOrm.target).label("target"),
            )
            .where(DailyTurnoverPerformanceOrm.trading_date >= threshold_date)
            .group_by(DailyTurnoverPerformanceOrm.trading_date)
            .order_by(DailyTurnoverPerformanceOrm.trading_date)
        )
        qs = rolewise_branch_data_filter(qs, current_user, DailyTurnoverPerformanceOrm)
        rows = session.execute(qs).all()

        results = [
            DailyTurnoverPerformance.model_validate(row._asdict()).model_dump()
            for row in rows
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_turnover_performance_statistics_by_branchid(
    request: Request, id: int
) -> Response:
    """fetch the turnover performance statistics for all"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                DailyTurnoverPerformanceOrm.trading_date.label("label"),
                func.sum(DailyTurnoverPerformanceOrm.generated).label("generated"),
                func.sum(DailyTurnoverPerformanceOrm.target).label("target"),
            )
            .where(DailyTurnoverPerformanceOrm.branch_code == id)
            .group_by(DailyTurnoverPerformanceOrm.trading_date)
            .order_by(DailyTurnoverPerformanceOrm.trading_date)
        )

        rows = session.execute(qs).all()

        results = [
            DailyTurnoverPerformance.model_validate(row._asdict()).model_dump()
            for row in rows
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margin_loan_statistics(request: Request) -> Response:
    """fetch the margin loan statistics for all"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = (
            select(
                DailyMarginLoanUsageOrm.trading_date.label("label"),
                func.sum(DailyMarginLoanUsageOrm.loan_amount).label("total_allocated"),
                func.sum(DailyMarginLoanUsageOrm.daily_turnover).label("daily_usage"),
            )
            .group_by(DailyMarginLoanUsageOrm.trading_date)
            .order_by(DailyMarginLoanUsageOrm.trading_date)
        )

        qs = rolewise_branch_data_filter(qs, current_user, DailyMarginLoanUsageOrm)

        rows = session.execute(qs).all()

        results = [
            DailyMarginLoanUsage.model_validate(row._asdict()).model_dump()
            for row in rows
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margin_loan_statistics_by_branchid(request: Request, id: int) -> Response:
    """fetch the margin loan statistics for branch"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user  # noqa: F841

    with Session(engine) as session:
        qs = (
            select(
                DailyMarginLoanUsageOrm.trading_date.label("label"),
                func.sum(DailyMarginLoanUsageOrm.loan_amount).label("total_allocated"),
                func.sum(DailyMarginLoanUsageOrm.daily_turnover).label("daily_usage"),
            )
            .where(DailyMarginLoanUsageOrm.branch_code == id)
            .group_by(DailyMarginLoanUsageOrm.trading_date)
            .order_by(DailyMarginLoanUsageOrm.trading_date)
        )
        rows = session.execute(qs).all()

        results = [
            DailyMarginLoanUsage.model_validate(row._asdict()).model_dump()
            for row in rows
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_cashcode_sector_exposure(request: Request) -> Response:
    """fetch the margin loan statistics for all"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user  # noqa: F841

    with Session(engine) as session:
        qs = (
            select(
                SectorExposureCashCodeOrm.sector_name.label("name"),
                func.sum(SectorExposureCashCodeOrm.total_qty).label("value"),
            )
            .group_by(SectorExposureCashCodeOrm.sector_name)
            .order_by(desc(text("value")))
        )

        qs = rolewise_branch_data_filter(qs, current_user, SectorExposureCashCodeOrm)

        rows = session.execute(qs).all()

        results = [
            SectorExposure.model_validate(row._asdict()).model_dump() for row in rows
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_cashcode_sector_exposure_by_branchid(request: Request, id: int) -> Response:
    """fetch the margin loan statistics for all"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user  # noqa: F841

    with Session(engine) as session:
        qs = (
            select(
                SectorExposureCashCodeOrm.sector_name.label("name"),
                func.sum(SectorExposureCashCodeOrm.total_qty).label("value"),
            )
            .where(SectorExposureCashCodeOrm.branch_code == id)
            .group_by(SectorExposureCashCodeOrm.sector_name)
            .order_by(desc(text("value")))
        )
        rows = session.execute(qs).all()

        results = [
            SectorExposure.model_validate(row._asdict()).model_dump() for row in rows
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margincode_sector_exposure(request: Request) -> Response:
    """fetch the margin loan statistics for all"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user  # noqa: F841

    with Session(engine) as session:
        qs = (
            select(
                SectorExposureMarginCodeOrm.sector_name.label("name"),
                func.sum(SectorExposureMarginCodeOrm.total_qty).label("value"),
            )
            .group_by(SectorExposureMarginCodeOrm.sector_name)
            .order_by(desc(text("value")))
        )

        qs = rolewise_branch_data_filter(qs, current_user, SectorExposureMarginCodeOrm)

        rows = session.execute(qs).all()

        results = [
            SectorExposure.model_validate(row._asdict()).model_dump() for row in rows
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.DTP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margincode_sector_exposure_by_branchid(request: Request, id: int) -> Response:
    """fetch the margin loan statistics for all"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user  # noqa: F841

    with Session(engine) as session:
        qs = (
            select(
                SectorExposureMarginCodeOrm.sector_name.label("name"),
                func.sum(SectorExposureMarginCodeOrm.total_qty).label("value"),
            )
            .where(SectorExposureMarginCodeOrm.branch_code == id)
            .group_by(SectorExposureMarginCodeOrm.sector_name)
            .order_by(desc(text("value")))
        )
        rows = session.execute(qs).all()

        results = [
            SectorExposure.model_validate(row._asdict()).model_dump() for row in rows
        ]

    return Response(results)
