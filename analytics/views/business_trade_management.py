from http import HTTPMethod

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.metadata.openapi import OpenApiTags
from core.permissions import ExtendedIsAdminUser
from core.renderer import CustomRenderer
from db import engine

from ..models import (
    ATBMarketShareSME,
    BoardTurnOver,
    BoardTurnOverBreakdown,
    CompanyWiseSaleableStock,
    CompanyWiseSaleableStockPercentage,
    InvestorWiseSaleableStock,
    MarketShareLBSL,
)
from ..orm import (
    ATBMarketShareSMEOrm,
    BoardTurnOverBreakdownOrm,
    BoardTurnOverOrm,
    CompanyWiseSaleableStockOrm,
    CompanyWiseSaleableStockPercentageOrm,
    InvestorWiseSaleableStockOrm,
    MarketShareLBSLOrm,
)


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_board_turnovers(request: Request) -> Response:
    """fetch branch turnovers"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(BoardTurnOverOrm).order_by(BoardTurnOverOrm.board)
        ).scalars()

        results = [BoardTurnOver.model_validate(row).model_dump() for row in qs]

    return Response(results)


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_board_turnovers_breakdown(request: Request) -> Response:
    """fetch branch turnovers breakdowns"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(BoardTurnOverBreakdownOrm).order_by(BoardTurnOverBreakdownOrm.board)
        ).scalars()

        results = [
            BoardTurnOverBreakdown.model_validate(row).model_dump() for row in qs
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_market_share_details(request: Request) -> Response:
    """fetch lbsl market share details"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            session.execute(
                select(MarketShareLBSLOrm).order_by(MarketShareLBSLOrm.trading_date)
            )
            .scalars()
            .one()
        )

        return Response(MarketShareLBSL.model_validate(qs).model_dump())


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_atb_markte_share_details(request: Request) -> Response:
    """fetch lbsl atb market share details"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            session.execute(
                select(ATBMarketShareSMEOrm).order_by(ATBMarketShareSMEOrm.trading_date)
            )
            .scalars()
            .one()
        )

        return Response(ATBMarketShareSME.model_validate(qs).model_dump())


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_company_wise_saleable_stock(request: Request) -> Response:
    """fetch company wise saleable stock"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(CompanyWiseSaleableStockOrm).order_by(
                CompanyWiseSaleableStockOrm.stock_available.desc()
            )
        ).scalars()

        results = [
            CompanyWiseSaleableStock.model_validate(row).model_dump() for row in qs
        ]

        return Response(results)


class InvestorStockPagination(PageNumberPagination):
    page_size = 50  # Customize the page size
    page_size_query_param = "page_size"  # Allow clients to control page size
    max_page_size = 100  # Max limit to prevent very large queries


@extend_schema(
    tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT],
    parameters=[
        OpenApiParameter(
            name="page", description="Page number", required=False, type=int
        ),
        OpenApiParameter(
            name="page_size",
            description="Number of results per page",
            required=False,
            type=int,
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_investor_wise_saleable_stock(request: Request) -> Response:
    """fetch investor wise saleable stock"""
    request.accepted_renderer = CustomRenderer()
    paginator = InvestorStockPagination()

    with Session(engine) as session:
        qs = (
            session.execute(
                select(InvestorWiseSaleableStockOrm).order_by(
                    InvestorWiseSaleableStockOrm.stock_available.desc()
                )
            )
            .scalars()
            .all()
        )
        paginated_results = paginator.paginate_queryset(qs, request)
        results = [
            InvestorWiseSaleableStock.model_validate(row).model_dump()
            for row in paginated_results
        ]
        return paginator.get_paginated_response(results)


@extend_schema(
    tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT],
    parameters=[
        OpenApiParameter(
            name="page", description="Page number", required=False, type=int
        ),
        OpenApiParameter(
            name="page_size",
            description="Number of results per page",
            required=False,
            type=int,
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_company_wise_saleable_stock_percentage(request: Request) -> Response:
    """fetch company wise saleable stock percentage"""
    request.accepted_renderer = CustomRenderer()
    paginator = InvestorStockPagination()

    with Session(engine) as session:
        qs = (
            session.execute(
                select(CompanyWiseSaleableStockPercentageOrm).order_by(
                    CompanyWiseSaleableStockPercentageOrm.stock_available.desc()
                )
            )
            .scalars()
            .all()
        )
        paginated_results = paginator.paginate_queryset(qs, request)
        results = [
            CompanyWiseSaleableStockPercentage.model_validate(row).model_dump()
            for row in paginated_results
        ]
        return paginator.get_paginated_response(results)
