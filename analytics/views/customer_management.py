from http import HTTPMethod
from typing import Any, Dict, Sequence

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.metadata.openapi import OpenApiTags
from core.permissions import IsManagementUser
from core.renderer import CustomRenderer
from db import engine

from ..models import (
    AdminBMClientSegmentationEquity,
    AdminBMClientSegmentationLedger,
    AdminBMClientSegmentationTPV,
    AdminBMClientSegmentationTurnover,
    AdminMarketShare,
    BranchWiseClientNumbers,
    ClientSegmentationSummary,
    NonPerformerClient,
    AdminGsecTurnover,
    AdminGsecTurnoverComparison,
)
from ..orm import (
    AdminBMClientSegmentationEquityOrm,
    AdminBMClientSegmentationLedgerOrm,
    AdminBMClientSegmentationTPVOrm,
    AdminBMClientSegmentationTurnoverOrm,
    AdminMarketShareOrm,
    BranchWiseClientNumbersOrm,
    ClientSegmentationSummaryOrm,
    NonPerformerClientOrm,
    AdminGsecTurnoverOrm,
    AdminGsecTurnoverComparisonOrm,

)


def get_sum_of_property(property: str, rows: Sequence[Dict[str, Any]]) -> int:
    sum = 0
    for row in rows:
        sum += row.get(property, 0)
    return round(sum)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_client_segmentation_summary(request: Request) -> Response:
    """fetch client segmentation summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(ClientSegmentationSummaryOrm).order_by(
                ClientSegmentationSummaryOrm.total_clients.desc()
            )
        ).scalars()

        results = [
            ClientSegmentationSummary.model_validate(row).model_dump() for row in qs
        ]

    response = {
        "detail": {
            "sum_of_clients": get_sum_of_property("total_clients", results),
        },
        "rows": results,
    }

    return Response(response)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_branchwise_client_numbers_ratio(request: Request) -> Response:
    """fetch branch turnovers"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(BranchWiseClientNumbersOrm).order_by(
                BranchWiseClientNumbersOrm.total_clients.desc()
            )
        ).scalars()

        results = [
            BranchWiseClientNumbers.model_validate(row).model_dump() for row in qs
        ]

    response = {
        "detail": {
            "sum_of_clients": get_sum_of_property("total_clients", results),
            "sum_of_clients_percentage": get_sum_of_property(
                "total_client_percentage", results
            ),
        },
        "rows": results,
    }

    return Response(response)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_non_performers_client_ratio(request: Request) -> Response:
    """fetch non performers clients"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(NonPerformerClientOrm).order_by(
                NonPerformerClientOrm.total_clients.desc()
            )
        ).scalars()

        results = [NonPerformerClient.model_validate(row).model_dump() for row in qs]

    response = {
        "detail": {
            "sum_of_clients": get_sum_of_property("total_clients", results),
            "sum_of_clients_percentage": get_sum_of_property(
                "total_client_percentage", results
            ),
        },
        "rows": results,
    }

    return Response(response)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_client_segmentation_turnover(request: Request) -> Response:
    """fetch admin client segmentation turnover ratio"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminBMClientSegmentationTurnoverOrm).order_by(
                AdminBMClientSegmentationTurnoverOrm.turnover.desc()
            )
        ).scalars()
        results = [
            AdminBMClientSegmentationTurnover.model_validate(row).model_dump()
            for row in qs
        ]

    response = {
        "detail": {
            "sum_of_turnovers": get_sum_of_property("turnover", results),
        },
        "rows": results,
    }

    return Response(response)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_client_segmentation_tpv(request: Request) -> Response:
    """fetch admin client segmentation tpv ratio"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminBMClientSegmentationTPVOrm).order_by(
                AdminBMClientSegmentationTPVOrm.tpv_total.desc()
            )
        ).scalars()

        results = [
            AdminBMClientSegmentationTPV.model_validate(row).model_dump() for row in qs
        ]

    response = {
        "detail": {
            "sum_of_free_qty": get_sum_of_property("free_qty", results),
            "sum_of_lock_qty": get_sum_of_property("lock_qty", results),
            "sum_of_tpv_total": get_sum_of_property("tpv_total", results),
            "sum_of_tpv_free_qty_percentage": get_sum_of_property(
                "tpv_free_qty_percentage", results
            ),
            "sum_of_tpv_lock_qty_percentage": get_sum_of_property(
                "tpv_lock_qty_percentage", results
            ),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_client_segmentation_equity(request: Request) -> Response:
    """fetch admin client segmentation equity ratio"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminBMClientSegmentationEquityOrm).order_by(
                AdminBMClientSegmentationEquityOrm.equity.desc()
            )
        ).scalars()

        results = [
            AdminBMClientSegmentationEquity.model_validate(row).model_dump()
            for row in qs
        ]
    response = {
        "detail": {
            "sum_of_equity": get_sum_of_property("equity", results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_client_segmentation_ledger(request: Request) -> Response:
    """fetch admin client segmentation ledger ratio"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminBMClientSegmentationLedgerOrm).order_by(
                AdminBMClientSegmentationLedgerOrm.margin.desc()
            )
        ).scalars()

        results = [
            AdminBMClientSegmentationLedger.model_validate(row).model_dump()
            for row in qs
        ]
    response = {
        "detail": {
            "sum_of_margin": get_sum_of_property("margin", results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_market_share(request: Request) -> Response:
    """fetch admin market share ratio"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminMarketShareOrm).order_by(
                AdminMarketShareOrm.year.asc(),
            )
        ).scalars()

        results = [AdminMarketShare.model_validate(row).model_dump() for row in qs]

    response = {
        "detail": {
            "sum_of_turnover_dse": get_sum_of_property("turnover_dse", results),
            "sum_of_turnover_lbsl": get_sum_of_property("turnover_lbsl", results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_gsec_turnover(request: Request) -> Response:
    """fetch admin gsec turnover"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminGsecTurnoverOrm).order_by(
                AdminGsecTurnoverOrm.trading_date.desc(),
            )
        ).scalars()

        results = [AdminGsecTurnover.model_validate(row).model_dump() for row in qs]

    response = {
        "detail": {
            "sum_of_turnover_gsec": get_sum_of_property("turnover_gsec", results),
        },
        "rows": results,
    }
    return Response(response)

@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_admin_gsec_turnover_comparison(request: Request) -> Response:
    """fetch admin gsec turnover comparison"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(AdminGsecTurnoverComparisonOrm).order_by(
                AdminGsecTurnoverComparisonOrm.year.desc(),
            )
        ).scalars()

        results = [AdminGsecTurnoverComparison.model_validate(row).model_dump() for row in qs]

    response = {
        "detail": {
            "sum_of_turnover_gsec": get_sum_of_property("turnover_gsec", results),
            "sum_of_turnover": get_sum_of_property("turnover", results),
        },
        "rows": results,
    }
    return Response(response)