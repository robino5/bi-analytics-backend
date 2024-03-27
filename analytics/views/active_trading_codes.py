from http import HTTPMethod

import pandas as pd
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.metadata.openapi import OpenApiTags
from core.permissions import ExtendedIsAdminUser
from core.renderer import CustomRenderer
from db import engine

from ..models import (
    ActiveTradingSummary,
)
from ..orm import (
    ActiveTradingCodeDayWiseSummaryORM,
    ActiveTradingCodeMonthWiseSummaryORM,
    ActiveTradingCodeSummaryORM,
)

__all__ = [
    "get_active_trading_summary",
    "get_active_trading_summary_daywise",
    "get_active_trading_monthwise_client",
]


@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_active_trading_summary(request: Request) -> Response:
    """fetch branch wise turnover status"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(ActiveTradingCodeSummaryORM).order_by(
                ActiveTradingCodeSummaryORM.trading_date
            )
        ).scalars()

        results = [ActiveTradingSummary.model_validate(row).model_dump() for row in qs]

    return Response(results)


@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_active_trading_summary_daywise(request: Request) -> Response:
    """fetch branch wise turnover status"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(ActiveTradingCodeDayWiseSummaryORM).order_by(
                ActiveTradingCodeDayWiseSummaryORM.trading_date
            )
        ).scalars()

        results = [ActiveTradingSummary.model_validate(row).model_dump() for row in qs]

    return Response(results)


@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_active_trading_monthwise_client(request: Request) -> Response:
    """fetch branch wise turnover status"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(
                ActiveTradingCodeMonthWiseSummaryORM.month_year,
                ActiveTradingCodeMonthWiseSummaryORM.channel,
                func.sum(ActiveTradingCodeMonthWiseSummaryORM.total_clients).label(
                    "total_clients"
                ),
                func.sum(ActiveTradingCodeMonthWiseSummaryORM.trades).label(
                    "total_trades"
                ),
                func.sum(ActiveTradingCodeMonthWiseSummaryORM.total_turnover).label(
                    "total_turnover"
                ),
            )
            .group_by(
                ActiveTradingCodeMonthWiseSummaryORM.channel,
                ActiveTradingCodeMonthWiseSummaryORM.month_year,
            )
            .order_by(ActiveTradingCodeMonthWiseSummaryORM.month_year)
        )

        df = pd.DataFrame([row._asdict() for row in qs], columns=qs.keys())

        total_clients = (
            df.pivot_table(
                index="month_year",
                columns="channel",
                values="total_clients",
                aggfunc="sum",
            )
            .reset_index()
            .to_dict(orient="records")
        )
        total_trades = (
            df.pivot_table(
                index="month_year",
                columns="channel",
                values="total_trades",
                aggfunc="sum",
            )
            .reset_index()
            .to_dict(orient="records")
        )
        total_turnover = (
            df.pivot_table(
                index="month_year",
                columns="channel",
                values="total_turnover",
                aggfunc="sum",
            )
            .reset_index()
            .to_dict(orient="records")
        )

        results = {
            "total_clients": total_clients,
            "total_trades": total_trades,
            "total_turnover": total_turnover,
        }

    return Response(results)
