from datetime import datetime
from enum import StrEnum
from http import HTTPMethod
from typing import Type

from django.http import HttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, literal, select
from sqlalchemy.orm import Session

from authusers.models import User
from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer
from db import engine

from ..models import Exposure, MarginLoanUsgae, MarkedInvestor, RMWiseNetTrade
from ..orm import (
    ExposureControllingManagementOrm,
    MarginLoanAllocationUsageOrm,
    NegativeEquityInvestorOrm,
    RedZoneInvestorOrm,
    RMWiseNetTradeOrm,
    YellowZoneInvestorOrm,
)
from .utils import generate_csv, rolewise_branch_data_filter

__all__ = [
    "get_margin_loan_allocations",
    "get_margin_loan_allocations_by_branchid",
    "get_exposures_list",
    "get_exposures_list_by_branchid",
    "get_rmwise_net_trades",
    "get_rmwise_net_trades_by_branch_id",
    "get_zone_marked_clients",
    "export_zone_marked_clients_csv",
]


class MarkedInvestorEnum(StrEnum):
    RED = "red"
    YELLOW = "yellow"
    NEGATIVE_EQUITY = "negative_equity"


InvestorOrmType = RedZoneInvestorOrm | YellowZoneInvestorOrm | NegativeEquityInvestorOrm


def get_marked_investors(
    investor_cls: Type[InvestorOrmType],
    user: User | None,
    branch_code: int | None = None,
):
    marginable_columns = (
        "marginable_exposure",
        "marginable_equity",
        "marginable_loan_ratio",
        "stock_value",
        "last_trading_dt",
        "acc_type",
        "branch_name",
    )
    qs = select(
        investor_cls.branch_code,
        func.trim(investor_cls.investor_code).label(
            "investor_code"
        ),  # db has whitespace in values
        func.trim(investor_cls.investor_name).label(
            "investor_name"
        ),  # db has whitespace in values
        investor_cls.ledger_balance,
        investor_cls.rm_name,
        investor_cls.exposure,
        investor_cls.equity,
        investor_cls.loan_ratio,
        *(
            getattr(investor_cls, column, literal(None).label(column))
            for column in marginable_columns
        ),
    ).order_by(investor_cls.investor_name)

    if user is not None:
        qs = rolewise_branch_data_filter(qs, user, investor_cls)
    if branch_code:
        qs = qs.where(investor_cls.branch_code == branch_code)

    return qs


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margin_loan_allocations(request: Request) -> Response:
    """fetch all margin loan allocation summary"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = (
            select(
                MarginLoanAllocationUsageOrm.col2.label("perticular"),
                func.sum(MarginLoanAllocationUsageOrm.col1).label("amount"),
            )
            .group_by(MarginLoanAllocationUsageOrm.col2)
            .order_by(MarginLoanAllocationUsageOrm.col2)
        )

        qs = rolewise_branch_data_filter(qs, current_user, MarginLoanAllocationUsageOrm)

        rows = session.execute(qs)
        results = [
            MarginLoanUsgae.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_margin_loan_allocations_by_branchid(request: Request, id: int) -> Response:
    """fetch all margin loan allocation summary by brnach id"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                MarginLoanAllocationUsageOrm.col2.label("perticular"),
                func.sum(MarginLoanAllocationUsageOrm.col1).label("amount"),
            )
            .where(MarginLoanAllocationUsageOrm.branch_code == id)
            .group_by(MarginLoanAllocationUsageOrm.col2)
            .order_by(MarginLoanAllocationUsageOrm.col2)
        )
        rows = session.execute(qs)
        results = [
            MarginLoanUsgae.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_exposures_list(request: Request) -> Response:
    """fetch all margin loan allocation summary"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = (
            select(
                ExposureControllingManagementOrm.exposure_type.label("exposure"),
                func.sum(ExposureControllingManagementOrm.investors_count).label(
                    "investors"
                ),
                func.sum(ExposureControllingManagementOrm.loan_amount).label(
                    "loan_amount"
                ),
            )
            .group_by(ExposureControllingManagementOrm.exposure_type)
            .order_by(ExposureControllingManagementOrm.exposure_type)
        )

        qs = rolewise_branch_data_filter(
            qs, current_user, ExposureControllingManagementOrm
        )

        rows = session.execute(qs)
        results = [Exposure.model_validate(row._asdict()).model_dump() for row in rows]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_exposures_list_by_branchid(request: Request, id: int) -> Response:
    """fetch all margin loan allocation summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                ExposureControllingManagementOrm.exposure_type.label("exposure"),
                func.sum(ExposureControllingManagementOrm.investors_count).label(
                    "investors"
                ),
                func.sum(ExposureControllingManagementOrm.loan_amount).label(
                    "loan_amount"
                ),
            )
            .where(ExposureControllingManagementOrm.branch_code == id)
            .group_by(ExposureControllingManagementOrm.exposure_type)
            .order_by(ExposureControllingManagementOrm.exposure_type)
        )
        rows = session.execute(qs)
        results = [Exposure.model_validate(row._asdict()).model_dump() for row in rows]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_rmwise_net_trades(request: Request) -> Response:
    """fetch all RM list with net trades"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = select(
            RMWiseNetTradeOrm.branch_code,
            RMWiseNetTradeOrm.branch_name,
            RMWiseNetTradeOrm.investor_code,
            RMWiseNetTradeOrm.opening_balance,
            RMWiseNetTradeOrm.ending_balance,
            RMWiseNetTradeOrm.net_buysell,
            RMWiseNetTradeOrm.rm_name,
        ).order_by(RMWiseNetTradeOrm.branch_name)

        qs = rolewise_branch_data_filter(qs, current_user, RMWiseNetTradeOrm)

        rows = session.execute(qs)
        results = [
            RMWiseNetTrade.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.MLU])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_rmwise_net_trades_by_branch_id(request: Request, id: int) -> Response:
    """fetch all RM list with net trades"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = (
            select(
                RMWiseNetTradeOrm.branch_code,
                RMWiseNetTradeOrm.branch_name,
                RMWiseNetTradeOrm.investor_code,
                RMWiseNetTradeOrm.opening_balance,
                RMWiseNetTradeOrm.ending_balance,
                RMWiseNetTradeOrm.net_buysell,
                RMWiseNetTradeOrm.rm_name,
            )
            .where(RMWiseNetTradeOrm.branch_code == id)
            .order_by(RMWiseNetTradeOrm.branch_name)
        )

        qs = rolewise_branch_data_filter(qs, current_user, RMWiseNetTradeOrm)

        rows = session.execute(qs)
        results = [
            RMWiseNetTrade.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.MLU],
    parameters=[
        OpenApiParameter(
            "investor_type",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="Type of the Investors to get",
            enum=MarkedInvestorEnum,
            allow_blank=False,
        ),
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="marked investors under specific branch",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_zone_marked_clients(request: Request) -> Response:
    """fetch all RM list with net trades"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    mark = request.query_params.get("investor_type")
    has_branch = request.query_params.get("branch")

    with Session(engine) as session:
        match mark:
            case MarkedInvestorEnum.RED:
                qs = get_marked_investors(RedZoneInvestorOrm, current_user, has_branch)
            case MarkedInvestorEnum.YELLOW:
                qs = get_marked_investors(
                    YellowZoneInvestorOrm, current_user, has_branch
                )
            case _:
                qs = get_marked_investors(
                    NegativeEquityInvestorOrm, current_user, has_branch
                )

        rows = session.execute(qs)
        results = [
            MarkedInvestor.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.MLU],
    parameters=[
        OpenApiParameter(
            "investor_type",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="Type of the investors to export",
            enum=MarkedInvestorEnum,
            allow_blank=False,
        ),
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="Export marked investors under a specific branch",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@authentication_classes([])
@permission_classes([AllowAny])
def export_zone_marked_clients_csv(request: Request) -> HttpResponse:
    """Export zone-marked investor data as a CSV that can be opened in Excel."""
    mark = request.query_params.get("investor_type")
    branch_code = request.query_params.get("branch")

    match mark:
        case MarkedInvestorEnum.RED:
            investor_cls = RedZoneInvestorOrm
            zone_name = MarkedInvestorEnum.RED
        case MarkedInvestorEnum.YELLOW:
            investor_cls = YellowZoneInvestorOrm
            zone_name = MarkedInvestorEnum.YELLOW
        case _:
            investor_cls = NegativeEquityInvestorOrm
            zone_name = MarkedInvestorEnum.NEGATIVE_EQUITY

    with Session(engine) as session:
        rows = session.execute(
            get_marked_investors(investor_cls, None, branch_code)
        )
        results = [
            MarkedInvestor.model_validate(row._asdict()).model_dump() for row in rows
        ]

    header_mapping = {
        "investor_code": "Investor Code",
        "investor_name": "Investor Name",
        "branch_name": "Branch Name",
        "ledger_balance": "Ledger Balance",
        "rm_name": "RM Name",
        "exposure": "Exposure",
        "equity": "Equity",
        "loan_ratio": "Loan Ratio",
        "marginable_exposure": "Marginable Exposure",
        "marginable_equity": "Marginable Equity",
        "marginable_loan_ratio": "Marginable Loan Ratio",
        "stock_value": "Stock Value",
        "last_trading_dt": "Last Trading Date",
        "acc_type": "Account Type",
    }
    remapped_results = [
        {header: row.get(field) for field, header in header_mapping.items()}
        for row in results
    ]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"zonewise-investors-{zone_name}-{timestamp}"
    return generate_csv(remapped_results, list(header_mapping.values()), filename)
