from http import HTTPMethod
from urllib.parse import urlencode

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.metadata.openapi import OpenApiTags
from core.permissions import IsManagementUser
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


class StockPagination(PageNumberPagination):
    page_size = 50  # Customize the page size
    page_size_query_param = "page_size"  # Allow clients to control page size
    max_page_size = 100  # Max limit to prevent very large queries


def _sanitaize_query_param(query: str) -> str | None:
    if query != "''" and query != '""' and query != "" and query:
        return query
    return None


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_board_turnovers(request: Request) -> Response:
    """fetch branch turnovers"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(BoardTurnOverOrm).order_by(BoardTurnOverOrm.turnover.desc())
        ).scalars()

        results = [BoardTurnOver.model_validate(row).model_dump() for row in qs]

    return Response(results)


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_board_turnovers_breakdown(request: Request) -> Response:
    """fetch branch turnovers breakdowns"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(BoardTurnOverBreakdownOrm).order_by(
                BoardTurnOverBreakdownOrm.turnover.desc()
            )
        ).scalars()

        results = [
            BoardTurnOverBreakdown.model_validate(row).model_dump() for row in qs
        ]

    return Response(results)


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_market_share_details(request: Request) -> Response:
    """fetch lbsl market share details"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            session.execute(
                select(MarketShareLBSLOrm).order_by(
                    MarketShareLBSLOrm.trading_date.desc()
                )
            )
            .scalars()
            .one()
        )

        return Response(MarketShareLBSL.model_validate(qs).model_dump())


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_atb_markte_share_details(request: Request) -> Response:
    """fetch lbsl atb market share details"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            session.execute(
                select(ATBMarketShareSMEOrm).order_by(
                    ATBMarketShareSMEOrm.trading_date.desc()
                )
            )
            .scalars()
            .one()
        )

        return Response(ATBMarketShareSME.model_validate(qs).model_dump())


@extend_schema(
    tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT],
    parameters=[
        OpenApiParameter(
            name="company", description="Company", required=False, type=str
        ),
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
@permission_classes([IsAuthenticated, IsManagementUser])
def get_company_wise_saleable_stock(request: Request) -> Response:
    """fetch company wise saleable stock"""
    request.accepted_renderer = CustomRenderer()
    paginator = StockPagination()

    company_q = _sanitaize_query_param(request.query_params.get("company"))

    with Session(engine) as session:
        query = select(CompanyWiseSaleableStockOrm).order_by(
            CompanyWiseSaleableStockOrm.company_name.asc()
        )

        if company_q:
            query = query.where(
                CompanyWiseSaleableStockOrm.company_name.ilike(f"%{company_q}%")
            )

        qs = session.execute(query).scalars().all()

        paginated_queryset = paginator.paginate_queryset(qs, request)
        results = [
            CompanyWiseSaleableStock.model_validate(row).model_dump()
            for row in paginated_queryset
        ]

        return paginator.get_paginated_response(results)


@extend_schema(
    tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT],
    parameters=[
        OpenApiParameter(
            name="company", description="Company", required=False, type=str
        ),
        OpenApiParameter(
            name="investor", description="Investor Code", required=False, type=str
        ),
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
@permission_classes([IsAuthenticated, IsManagementUser])
def get_investor_wise_saleable_stock(request: Request) -> Response:
    """fetch investor wise saleable stock"""
    request.accepted_renderer = CustomRenderer()

    company_q = _sanitaize_query_param(request.query_params.get("company"))
    investor_q = _sanitaize_query_param(request.query_params.get("investor"))
    # Get pagination info from request
    page_number = request.query_params.get("page", 1)
    page_size = request.query_params.get("page_size", 10)
    offset = (int(page_number) - 1) * int(page_size)

    with Session(engine) as session:
        query = select(InvestorWiseSaleableStockOrm).order_by(
            InvestorWiseSaleableStockOrm.company_name.asc(),
            InvestorWiseSaleableStockOrm.branch_name.asc(),
        )
        if company_q:
            query = query.where(
                InvestorWiseSaleableStockOrm.company_name.ilike(f"%{company_q}%")
            )
        if investor_q:
            query = query.where(
                InvestorWiseSaleableStockOrm.investor_code.ilike(f"{investor_q}")
            )
        # Count total rows for pagination metadata
        total_count = session.execute(
            select(func.count()).select_from(query.subquery())
        ).scalar()
        # Apply pagination at the SQLAlchemy level
        query = query.offset(offset).limit(page_size)

        qs = session.execute(query).scalars().all()

        results = [
            InvestorWiseSaleableStock.model_validate(row).model_dump() for row in qs
        ]

        # Construct next and previous URLs
        def build_page_url(page):
            # Keep existing query parameters but modify the "page"
            query_params = request.query_params.copy()
            query_params["page"] = page
            return request.build_absolute_uri(f"?{urlencode(query_params)}")

        next_url = (
            build_page_url(int(page_number) + 1)
            if offset + int(page_size) < total_count
            else None
        )
        previous_url = (
            build_page_url(int(page_number) - 1) if int(page_number) > 1 else None
        )

        # Construct custom paginated response
        response_data = {
            "count": total_count,
            "total_pages": (total_count // int(page_size))
            + (1 if total_count % int(page_size) > 0 else 0),
            "next": next_url,
            "previous": previous_url,
            "current_page": int(page_number),
            "page_size": page_size,
            "results": results,
        }

        return Response(response_data)


@extend_schema(
    tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT],
    parameters=[
        OpenApiParameter(
            name="company", description="Company", required=False, type=str
        ),
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
@permission_classes([IsAuthenticated, IsManagementUser])
def get_company_wise_saleable_stock_percentage(request: Request) -> Response:
    """fetch company wise saleable stock percentage"""
    request.accepted_renderer = CustomRenderer()
    paginator = StockPagination()

    company_q = _sanitaize_query_param(request.query_params.get("company"))

    with Session(engine) as session:
        query = select(CompanyWiseSaleableStockPercentageOrm).order_by(
            CompanyWiseSaleableStockPercentageOrm.company_name.asc(),
            CompanyWiseSaleableStockPercentageOrm.branch_name.asc(),
        )

        if company_q:
            query = query.where(
                CompanyWiseSaleableStockPercentageOrm.company_name.ilike(
                    f"%{company_q}%"
                )
            )

        qs = session.execute(query).scalars().all()
        paginated_results = paginator.paginate_queryset(qs, request)
        results = [
            CompanyWiseSaleableStockPercentage.model_validate(row).model_dump()
            for row in paginated_results
        ]
        return paginator.get_paginated_response(results)
