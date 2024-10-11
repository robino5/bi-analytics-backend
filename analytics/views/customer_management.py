from http import HTTPMethod

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
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
    AdminBMClientSegmentationEquity,
    AdminBMClientSegmentationLedger,
    AdminBMClientSegmentationTPV,
    AdminBMClientSegmentationTurnover,
    AdminMarketShare,
    BranchWiseClientNumbers,
    ClientSegmentationSummary,
    NonPerformerClient,
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
)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
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

    return Response(results)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
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

    return Response(results)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
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

        return Response(results)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
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
        return Response(results)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
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

        return Response(results)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
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

        return Response(results)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
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
        return Response(results)


@extend_schema(tags=[OpenApiTags.ADMIN_CUSTOMER_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
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
        return Response(results)
