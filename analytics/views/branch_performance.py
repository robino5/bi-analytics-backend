from http import HTTPMethod

import pandas as pd
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from authusers.models import User
from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer
from db import engine

from ..models import (
    BranchWiseFundStatus,
    BranchWiseMarginStatus,
    BranchWiseTurnoverStatus,
)
from ..orm import (
    BranchWiseFundStatusOrm,
    BranchWiseMarginExposureStatusOrm,
    BranchWiseMarginStatusOrm,
    BranchWiseTurnoverStatusOrm,
)
from .utils import rolewise_branch_data_filter

__all__ = [
    "get_bw_turnover_status",
    "get_bw_margin_status",
    "get_bw_fund_status",
    "get_bw_exposure_status",
]


@extend_schema(
    tags=[OpenApiTags.BP],
    parameters=[
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_bw_turnover_status(request: Request) -> Response:
    """fetch branch wise turnover status"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_branch = request.query_params.get("branch", None)

    with Session(engine) as session:
        qs = select(
            BranchWiseTurnoverStatusOrm.branch_code,
            BranchWiseTurnoverStatusOrm.branch_name,
            BranchWiseTurnoverStatusOrm.turnover_daily,
            BranchWiseTurnoverStatusOrm.turnover_weekly,
            BranchWiseTurnoverStatusOrm.turnover_monthly,
            BranchWiseTurnoverStatusOrm.turnover_yearly,
        ).order_by(BranchWiseTurnoverStatusOrm.branch_name)

        qs = rolewise_branch_data_filter(qs, current_user, BranchWiseTurnoverStatusOrm)

        if has_branch:
            qs = qs.where(BranchWiseTurnoverStatusOrm.branch_code == has_branch)

        rows = session.execute(qs)
        results = [
            BranchWiseTurnoverStatus.model_validate(row._asdict()).model_dump()
            for row in rows
        ]
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.BP],
    parameters=[
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_bw_margin_status(request: Request) -> Response:
    """fetch branch wise turnover status"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_branch = request.query_params.get("branch", None)

    with Session(engine) as session:
        qs = select(
            BranchWiseMarginStatusOrm.branch_code,
            BranchWiseMarginStatusOrm.branch_name,
            BranchWiseMarginStatusOrm.loan_used,
            BranchWiseMarginStatusOrm.turnover_daily,
            BranchWiseMarginStatusOrm.turnover_weekly,
            BranchWiseMarginStatusOrm.turnover_monthly,
            BranchWiseMarginStatusOrm.turnover_yearly,
        ).order_by(BranchWiseMarginStatusOrm.branch_name)

        qs = rolewise_branch_data_filter(qs, current_user, BranchWiseMarginStatusOrm)

        if has_branch:
            qs = qs.where(BranchWiseMarginStatusOrm.branch_code == has_branch)

        rows = session.execute(qs)
        results = [
            BranchWiseMarginStatus.model_validate(row._asdict()).model_dump()
            for row in rows
        ]
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.BP],
    parameters=[
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_bw_fund_status(request: Request) -> Response:
    """fetch branch wise fund status"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    has_branch = request.query_params.get("branch", None)

    with Session(engine) as session:
        qs = select(
            BranchWiseFundStatusOrm.branch_code,
            BranchWiseFundStatusOrm.branch_name,
            BranchWiseFundStatusOrm.tpv,
            BranchWiseFundStatusOrm.total_clients,
            BranchWiseFundStatusOrm.fund_in,
            BranchWiseFundStatusOrm.fund_withdrawl,
            BranchWiseFundStatusOrm.net_fundflow,
        ).order_by(BranchWiseFundStatusOrm.branch_name)

        qs = rolewise_branch_data_filter(qs, current_user, BranchWiseFundStatusOrm)

        if has_branch:
            qs = qs.where(BranchWiseFundStatusOrm.branch_code == has_branch)

        rows = session.execute(qs)
        results = [
            BranchWiseFundStatus.model_validate(row._asdict()).model_dump()
            for row in rows
        ]
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.BP],
    parameters=[
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_bw_exposure_status(request: Request) -> Response:
    """fetch branch wise fund status"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_branch = request.query_params.get("branch", None)

    with Session(engine) as session:
        qs = select(
            BranchWiseMarginExposureStatusOrm.branch_code,
            BranchWiseMarginExposureStatusOrm.branch_name,
            BranchWiseMarginExposureStatusOrm.exposure_type,
            BranchWiseMarginExposureStatusOrm.investors_count,
            BranchWiseMarginExposureStatusOrm.exposure_ratio,
        ).order_by(BranchWiseMarginExposureStatusOrm.branch_name)

        qs = rolewise_branch_data_filter(
            qs, current_user, BranchWiseMarginExposureStatusOrm
        )

        if has_branch:
            qs = qs.where(BranchWiseMarginExposureStatusOrm.branch_code == has_branch)

        rows = session.execute(qs)
        df = pd.DataFrame([row._asdict() for row in rows], columns=rows.keys())

        grouped_df = df.groupby(["branch_name", "exposure_type"])

        def _set_key_name(exposure_type: str) -> str:
            exp = exposure_type.lower()
            if "green" in exp:
                return "green"
            if "yellow" in exp:
                return "yellow"
            if "red" in exp:
                return "red"

        results = {}
        for (branch, exposure), group in grouped_df:
            branch_dict = results.setdefault(branch, {})
            branch_dict[_set_key_name(exposure)] = group.to_dict(orient="records")[0]

        data = []
        for key, value in results.items():
            prep_dict = {"branch_name": key, "exposures": value}
            data.append(prep_dict)
    return Response(data)
