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

from ..models import RMWiseClientDetail
from ..orm import RMWiseClientDetailOrm, RMWiseTurnoverPerformanceOrm
from .utils import inject_branchwise_filter

__all__ = ["get_turnover_perfomance_rmwise", "get_client_detail_rmwise"]


@extend_schema(
    tags=[OpenApiTags.RMWISE_PERFORMANCE],
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
            required=True,
            description="Username of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_turnover_perfomance_rmwise(request: Request) -> Response:
    """fetch summary of turnover performance"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    branch_query = request.query_params.get("branch_code", None)
    rm_id = request.query_params.get("username", None)

    with Session(engine) as session:
        qs = select(
            RMWiseTurnoverPerformanceOrm.branch_code,
            RMWiseTurnoverPerformanceOrm.branch_name,
            RMWiseTurnoverPerformanceOrm.col1,
            RMWiseTurnoverPerformanceOrm.col2,
            RMWiseTurnoverPerformanceOrm.col3,
        )

        qs = inject_branchwise_filter(qs, current_user, RMWiseTurnoverPerformanceOrm)

        if branch_query:
            qs = qs.where(
                RMWiseTurnoverPerformanceOrm.branch_code == branch_query,
            )
        if rm_id:
            qs = qs.where(
                RMWiseTurnoverPerformanceOrm.trader_id == rm_id,
            )
        rows = session.execute(qs)

        df = pd.DataFrame([row._asdict() for row in rows], columns=rows.keys())
        df["col2"] = df["col2"].str.strip()  # trim the col2, has space

        pivot_df = df.pivot_table(
            index="col2", columns="col3", values="col1", aggfunc="sum"
        ).reset_index()  # aggregate the df

        pivot_df.columns = map(str.lower, pivot_df.columns)

        pivot_df.rename(columns={"col2": "name"}, inplace=True)
    return Response(pivot_df.to_dict(orient="records"))


@extend_schema(
    tags=[OpenApiTags.RMWISE_PERFORMANCE],
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
            required=True,
            description="Username of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_client_detail_rmwise(request: Request) -> Response:
    """fetch the turnover performance statistics rm wise"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    branch_query = request.query_params.get("branch_code", None)
    rm_id = request.query_params.get("username", None)

    with Session(engine) as session:
        qs = select(RMWiseClientDetailOrm).order_by(RMWiseClientDetailOrm.trader_id)
        qs = inject_branchwise_filter(qs, current_user, RMWiseClientDetailOrm)

        if branch_query:
            qs = qs.where(
                RMWiseClientDetailOrm.branch_code == branch_query,
            )
        if rm_id:
            qs = qs.where(
                RMWiseClientDetailOrm.trader_id == rm_id,
            )
        rows = session.execute(qs).scalars()

        results = [RMWiseClientDetail.model_validate(row).model_dump() for row in rows]

    return Response(results)
