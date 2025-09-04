from http import HTTPMethod
from typing import Any, Dict
from datetime import datetime
from drf_spectacular.types import OpenApiTypes
import pandas as pd
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
    ActiveTradingSummary,
    AdminOMSBranchWiseTurnoverAsOnMonth,
    AdminOMSDateWiseTurnover,
    AdminSectorWiseTurnover,
    AdminSectorWiseTurnoverBreakdown,
    AdminRealTimeTurnoverTop20,
    AdminRealTimeTurnoverComparisonSectorWise,
    AdminRealTimeTurnoverExchangeTop20,
    AdminRealTimeTurnoverComparisonTop20SectorWise,
    AdminOMSBranchWiseTurnoverDtAsOnMonth


)
from ..orm import (
    ActiveTradingCodeDayWiseSummaryORM,
    ActiveTradingCodeMonthWiseSummaryORM,
    ActiveTradingCodeSummaryORM,
    AdminOMSBranchWiseTurnoverAsOnMonthORM,
    AdminOMSDateWiseTurnoverORM,
    AdminSectorWiseTurnoverORM,
    AdminSectorWiseTurnoverBreakdownORM,
    AdminRealTimeTurnoverTop20ORM,
    AdminRealTimeTurnoverComparisonSectorWiseORM,
    AdminRealTimeTurnoverExchangeTop20ORM,
    AdminRealTimeTurnoverComparisonTop20SectorWiseORM,
    AdminOMSBranchWiseTurnoverDtAsOnMonthORM
)

__all__ = [
    "get_active_trading_summary",
    "get_active_trading_summary_daywise",
    "get_active_trading_monthwise_client",
    "get_admin_oms_branch_wise_turnover_as_on_month",
    "get_admin_oms_datewise_turnover",
    "get_admin_sector_wise_turnover",
    "get_admin_sector_wise_turnover_breakdown",
    "get_admin_realtime_turnover_top_20",
    "get_admin_realtime_turnover_comaparison_sector_wise",
    "get_admin_realtime_turnover_exchange_top_20",
    "get_admin_realtime_turnover_comaparison_top20_sector_wise",
    "get_admin_oms_branch_wise_turnover_dt_as_on_month"

]

def get_sum_of_property(property: str, rows: Sequence[Dict[str, Any]]) -> int:
    sum = 0
    for row in rows:
        sum += row.get(property, 0)
    return round(sum)


@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
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
@permission_classes([IsAuthenticated, IsManagementUser])
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
@permission_classes([IsAuthenticated, IsManagementUser])
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

@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_oms_branch_wise_turnover_as_on_month(request: Request) -> Response:
    """fetch admin OMS Branch wise turnover as on month status"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminOMSBranchWiseTurnoverAsOnMonthORM).order_by(
                AdminOMSBranchWiseTurnoverAsOnMonthORM.branch_Name
            )
        ).scalars()

        results = [AdminOMSBranchWiseTurnoverAsOnMonth.model_validate(row).model_dump() for row in qs]

        
    response = {
        "detail": {
            "period":datetime.now().strftime("%B-%Y"),
            "sum_of_total_client_today": get_sum_of_property("active_clients_today", results),
            "sum_of_turnover_today": get_sum_of_property("turnover_today", results),
            "sum_of_total_client_month": get_sum_of_property("active_clients_month", results),
            "sum_of_turnover_month": get_sum_of_property("turnover_month", results),
        },
        "rows": results,
    }

    return Response(response)


@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_oms_branch_wise_turnover_dt_as_on_month(request: Request) -> Response:
    """fetch admin OMS Branch wise turnover Dt as on month status"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminOMSBranchWiseTurnoverDtAsOnMonthORM).order_by(
                AdminOMSBranchWiseTurnoverDtAsOnMonthORM.branch_Name
            )
        ).scalars()

        results = [AdminOMSBranchWiseTurnoverDtAsOnMonth.model_validate(row).model_dump() for row in qs]

        
    response = {
        "detail": {
            "period":datetime.now().strftime("%B-%Y"),
            "sum_of_total_client_today": get_sum_of_property("active_clients_today", results),
            "sum_of_turnover_today": get_sum_of_property("turnover_today", results),
            "sum_of_total_client_month": get_sum_of_property("active_clients_month", results),
            "sum_of_turnover_month": get_sum_of_property("turnover_month", results),
        },
        "rows": results,
    }

    return Response(response)


@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_oms_datewise_turnover(request: Request) -> Response:
    """fetch admin OMS Branch wise turnover as on month status"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminOMSDateWiseTurnoverORM).order_by(
                AdminOMSDateWiseTurnoverORM.trading_date.desc()
            )
        ).scalars()

        results = [AdminOMSDateWiseTurnover.model_validate(row).model_dump() for row in qs]

        
    response = {
        "detail": {
            "sum_of_total_client": get_sum_of_property("total_client", results),
            "sum_of_turnover": get_sum_of_property("total_turnover", results),
        },
        "rows": results,
    }
    
    return Response(response)

@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_sector_wise_turnover(request: Request) -> Response:
    """fetch admin sector wise turnover """
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminSectorWiseTurnoverORM).order_by(
                AdminSectorWiseTurnoverORM.value.desc()
            )
        ).scalars()

        results = [AdminSectorWiseTurnover.model_validate(row).model_dump() for row in qs]

    return Response(results)

@extend_schema(
    tags=[OpenApiTags.ACTIVE_TRADING_CODE],
    parameters=[
        OpenApiParameter(
            "sector_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="sector name",
        ),
    ],
)
@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_sector_wise_turnover_breakdown(request: Request) -> Response:
    """fetch admin sector wise turnover breakdown """
    request.accepted_renderer = CustomRenderer()

    has_sector_name= request.query_params.get("sector_name", None)

    with Session(engine) as session:
        qs = (
            select(AdminSectorWiseTurnoverBreakdownORM).order_by(
                AdminSectorWiseTurnoverBreakdownORM.value.desc()
            )
        )

        if has_sector_name:
         qs = qs.where(
        func.upper(AdminSectorWiseTurnoverBreakdownORM.sector_name) == func.upper(has_sector_name)
    )

        qs = session.execute(qs).scalars()

        results = [AdminSectorWiseTurnoverBreakdown.model_validate(row).model_dump() for row in qs]

    return Response(results)

@extend_schema(
    tags=[OpenApiTags.ACTIVE_TRADING_CODE],
    parameters=[
        OpenApiParameter(
            "trading_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Trading date in format YYYY-MM-DD",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_realtime_turnover_top_20(request: Request) -> Response:
    """fetch admin real time turnover top 20"""
    request.accepted_renderer = CustomRenderer()
    has_trading_date = request.query_params.get("trading_date")

    with Session(engine) as session:
        if has_trading_date:
            try:
                trading_date = datetime.strptime(has_trading_date, "%Y-%m-%d")
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        else:
            trading_date = session.execute(
                select(func.max(AdminRealTimeTurnoverTop20ORM.trading_date))
            ).scalar()

            if not trading_date:
                return Response([]) 
            
            
        qs = session.execute(
            select(AdminRealTimeTurnoverTop20ORM)
            .where(AdminRealTimeTurnoverTop20ORM.trading_date == trading_date)
            .order_by(AdminRealTimeTurnoverTop20ORM.value.desc())
            .limit(20)
        ).scalars()

        results = [AdminRealTimeTurnoverTop20.model_validate(row).model_dump() for row in qs]

    return Response(results)

@extend_schema(
    tags=[OpenApiTags.ACTIVE_TRADING_CODE],
    parameters=[
        OpenApiParameter(
            "trading_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Trading date in format YYYY-MM-DD",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_realtime_turnover_exchange_top_20(request: Request) -> Response:
    """fetch admin real time turnover exchange top 20"""
    request.accepted_renderer = CustomRenderer()
    has_trading_date = request.query_params.get("trading_date")

    with Session(engine) as session:
        if has_trading_date:
            try:
                trading_date = datetime.strptime(has_trading_date, "%Y-%m-%d")
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        else:
            trading_date = session.execute(
                select(func.max(AdminRealTimeTurnoverExchangeTop20ORM.trading_date))
            ).scalar()

            if not trading_date:
                return Response([]) 

        qs = session.execute(
            select(AdminRealTimeTurnoverExchangeTop20ORM)
            .where(AdminRealTimeTurnoverExchangeTop20ORM.trading_date == trading_date)
            .order_by(AdminRealTimeTurnoverExchangeTop20ORM.value.desc())
        ).scalars()

        results = [AdminRealTimeTurnoverExchangeTop20.model_validate(row).model_dump() for row in qs]

    return Response(results)


@extend_schema(
    tags=[OpenApiTags.ACTIVE_TRADING_CODE],
    parameters=[
        OpenApiParameter(
            "trading_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Trading date in format YYYY-MM-DD",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_realtime_turnover_comaparison_sector_wise(request: Request) -> Response:
    """Fetch admin real-time turnover comparison sector-wise for a given trading date or the latest trading date."""
    request.accepted_renderer = CustomRenderer()
    has_trading_date = request.query_params.get("trading_date")

    with Session(engine) as session:
        if has_trading_date:
            try:
                trading_date = datetime.strptime(has_trading_date, "%Y-%m-%d")
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        else:
            trading_date = session.execute(
                select(func.max(AdminRealTimeTurnoverComparisonSectorWiseORM.trading_date))
            ).scalar()

            if not trading_date:
                return Response([]) 

        qs = session.execute(
            select(AdminRealTimeTurnoverComparisonSectorWiseORM)
            .where(AdminRealTimeTurnoverComparisonSectorWiseORM.trading_date == trading_date)
            .order_by(AdminRealTimeTurnoverComparisonSectorWiseORM.primary_value.desc())
        ).scalars()

        results = [
            AdminRealTimeTurnoverComparisonSectorWise.model_validate(row).model_dump()
            for row in qs
        ]

    return Response(results)


@extend_schema(
    tags=[OpenApiTags.ACTIVE_TRADING_CODE],
    parameters=[
        OpenApiParameter(
            "trading_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Trading date in format YYYY-MM-DD",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_realtime_turnover_comaparison_top20_sector_wise(request: Request) -> Response:
    """fetch admin real time turnover comparison top 20 sector wise"""
    request.accepted_renderer = CustomRenderer()
    has_trading_date = request.query_params.get("trading_date")

    with Session(engine) as session:
        if has_trading_date:
            try:
                trading_date = datetime.strptime(has_trading_date, "%Y-%m-%d")
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        else:
            trading_date = session.execute(
                select(func.max(AdminRealTimeTurnoverComparisonTop20SectorWiseORM.trading_date))
            ).scalar()

            if not trading_date:
                return Response([]) 
    

        qs = session.execute(
            select(AdminRealTimeTurnoverComparisonTop20SectorWiseORM)
            .where(AdminRealTimeTurnoverComparisonTop20SectorWiseORM.trading_date == trading_date)
            .order_by(AdminRealTimeTurnoverComparisonTop20SectorWiseORM.primary_value.desc())
        ).scalars()

        results = [AdminRealTimeTurnoverComparisonTop20SectorWise.model_validate(row).model_dump() for row in qs]

    return Response(results)