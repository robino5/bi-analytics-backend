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

from ..models import RMWiseClientDetail,InvestroLiveNetTradeRMWise
from ..orm import RMWiseClientDetailOrm, RMWiseTurnoverPerformanceOrm,InvestroLiveNetTradeRMWiseOrm
from .utils import rolewise_branch_data_filter

__all__ = ["get_turnover_perfomance_rmwise", "get_client_detail_rmwise","get_investor_live_net_trade_rm_wise"]


@extend_schema(
    tags=[OpenApiTags.RMWISE_PERFORMANCE],
    parameters=[
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=True,
            description="Branch Code Of the RM",
        ),
        OpenApiParameter(
            "trader",
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

    has_branch = request.query_params.get("branch", None)
    has_trader = request.query_params.get("trader", None)

    with Session(engine) as session:
        qs = select(
            RMWiseTurnoverPerformanceOrm.branch_code,
            RMWiseTurnoverPerformanceOrm.branch_name,
            RMWiseTurnoverPerformanceOrm.col1,
            RMWiseTurnoverPerformanceOrm.col2,
            RMWiseTurnoverPerformanceOrm.col3,
        )

        qs = rolewise_branch_data_filter(qs, current_user, RMWiseTurnoverPerformanceOrm)

        if has_branch:
            qs = qs.where(
                RMWiseTurnoverPerformanceOrm.branch_code == has_branch,
            )
        if has_trader:
            qs = qs.where(
                RMWiseTurnoverPerformanceOrm.trader_id == has_trader,
            )
        rows = session.execute(qs)

        df = pd.DataFrame([row._asdict() for row in rows], columns=rows.keys())
        df["col2"] = df["col2"].str.strip()  # trim the col2, has space

        pivot_df = df.pivot_table(
            index="col2", columns="col3", values="col1", aggfunc="sum", fill_value=0
        ).reset_index()  # aggregate the df

        pivot_df.columns = map(str.lower, pivot_df.columns)

        pivot_df.rename(columns={"col2": "name"}, inplace=True)
    return Response(pivot_df.to_dict(orient="records"))


@extend_schema(
    tags=[OpenApiTags.RMWISE_PERFORMANCE],
    parameters=[
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=True,
            description="Branch Code Of the RM",
        ),
        OpenApiParameter(
            "trader",
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

    has_branch = request.query_params.get("branch", None)
    has_trader = request.query_params.get("trader", None)

    with Session(engine) as session:
        qs = select(RMWiseClientDetailOrm).order_by(RMWiseClientDetailOrm.trader_id)
        qs = rolewise_branch_data_filter(qs, current_user, RMWiseClientDetailOrm)

        if has_branch:
            qs = qs.where(
                RMWiseClientDetailOrm.branch_code == has_branch,
            )
        if has_trader:
            qs = qs.where(
                RMWiseClientDetailOrm.trader_id == has_trader,
            )
        rows = session.execute(qs).scalars()

        results = [RMWiseClientDetail.model_validate(row).model_dump() for row in rows]

    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RMWISE_PERFORMANCE],
    parameters=[
        OpenApiParameter(
            "branch",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="Branch Code Of the RM",
        ),
        OpenApiParameter(
            "trader",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="Username of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_investor_live_net_trade_rm_wise(request: Request) -> Response:
    """fetch the investor live net trade rm wise"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_branch = request.query_params.get("branch", None)
    has_trader = request.query_params.get("trader", None)

    with Session(engine) as session:
        qs = select(InvestroLiveNetTradeRMWiseOrm).order_by(InvestroLiveNetTradeRMWiseOrm.trader_id)
        qs = rolewise_branch_data_filter(qs, current_user, InvestroLiveNetTradeRMWiseOrm)

        if has_branch:
            qs = qs.where(
                InvestroLiveNetTradeRMWiseOrm.branch_code == has_branch,
            )
        if has_trader:
            qs = qs.where(
                InvestroLiveNetTradeRMWiseOrm.trader_id == has_trader,
            )
        rows = session.execute(qs).scalars()

        results = [InvestroLiveNetTradeRMWise.model_validate(row).model_dump() for row in rows]

    return Response(results)
