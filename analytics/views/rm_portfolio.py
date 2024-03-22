from enum import StrEnum
from http import HTTPMethod
from typing import Type

import pandas as pd
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from authusers.models import User
from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer
from db import engine

from ..models import DailyNetFundFlow, MarkedInvestor, PortfolioMangement
from ..orm import (
    RMWiseDailyNetFundFlowORM,
    RMWiseFundCollectionOrm,
    RMWisePortfolioMangementORM,
    RMWiseRedZoneTraderORM,
    RMWiseYellowZoneTraderORM,
)
from .utils import inject_branchwise_filter

__all__ = [
    "get_fund_collection_rmwise",
    "get_portfolio_management_rmwise",
    "get_daily_net_fund_flow_rmwise",
    "get_zone_marked_clients_rmwise",
]


InvestorOrmType = RMWiseYellowZoneTraderORM | RMWiseRedZoneTraderORM


def get_marked_investors(
    investor_cls: Type[InvestorOrmType],
    branch_code: int,
    trader: str,
):
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
    ).order_by(investor_cls.investor_name)

    if trader:
        qs = qs.where(investor_cls.rm_name == trader)

    if branch_code:
        qs = qs.where(investor_cls.branch_code == int(branch_code))

    return qs


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
            description="Trader Id of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_fund_collection_rmwise(request: Request) -> Response:
    """fetch summary of turnover performance"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_branch = request.query_params.get("branch", None)
    has_trader = request.query_params.get("trader", None)

    with Session(engine) as session:
        qs = select(
            RMWiseFundCollectionOrm.col1,
            RMWiseFundCollectionOrm.col2,
            RMWiseFundCollectionOrm.col3,
        )

        qs = inject_branchwise_filter(qs, current_user, RMWiseFundCollectionOrm)

        if has_branch:
            qs = qs.where(
                RMWiseFundCollectionOrm.branch_code == has_branch,
            )
        if has_trader:
            qs = qs.where(
                RMWiseFundCollectionOrm.trader_id == has_trader,
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
            description="Trader Id of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_portfolio_management_rmwise(request: Request) -> Response:
    """fetch summary of portfolio management status"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_branch = request.query_params.get("branch", None)
    has_trader = request.query_params.get("trader", None)

    with Session(engine) as session:
        qs = select(
            RMWisePortfolioMangementORM.particular_type.label("particular"),
            RMWisePortfolioMangementORM.amount,
        )

        qs = inject_branchwise_filter(qs, current_user, RMWisePortfolioMangementORM)

        if has_branch:
            qs = qs.where(
                RMWisePortfolioMangementORM.branch_code == has_branch,
            )
        if has_trader:
            qs = qs.where(
                RMWisePortfolioMangementORM.trader_id == has_trader,
            )
        rows = session.execute(qs)

        results = [
            PortfolioMangement.model_validate(row._asdict()).model_dump()
            for row in rows
        ]
    return Response(results)


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
            description="Trader Id of the RM",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_daily_net_fund_flow_rmwise(request: Request) -> Response:
    """fetch summary of portfolio management status"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_branch = request.query_params.get("branch", None)
    has_trader = request.query_params.get("trader", None)

    with Session(engine) as session:
        qs = select(
            RMWiseDailyNetFundFlowORM.trading_date.label("trading_date"),
            func.sum(RMWiseDailyNetFundFlowORM.fundflow).label("amount"),
        ).group_by(RMWiseDailyNetFundFlowORM.trading_date)

        qs = inject_branchwise_filter(qs, current_user, RMWiseDailyNetFundFlowORM)

        if has_branch:
            qs = qs.where(
                RMWiseDailyNetFundFlowORM.branch_code == has_branch,
            )
        if has_trader:
            qs = qs.where(
                RMWiseDailyNetFundFlowORM.trader_id == has_trader,
            )
        rows = session.execute(qs)
        results = [
            DailyNetFundFlow.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


class MarkedInvestorEnum(StrEnum):
    RED = "red"
    YELLOW = "yellow"


@extend_schema(
    tags=[OpenApiTags.RMWISE_PERFORMANCE],
    parameters=[
        OpenApiParameter(
            "category",
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
            required=True,
            description="marked investors under specific branch",
        ),
        OpenApiParameter(
            "trader",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="marked investors under specific trader",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_zone_marked_clients_rmwise(request: Request) -> Response:
    """fetch all RM list with net trades"""
    request.accepted_renderer = CustomRenderer()

    has_category = request.query_params.get("category", MarkedInvestorEnum.RED)
    has_branch = request.query_params.get("branch", None)
    has_trader = request.query_params.get("trader", None)

    with Session(engine) as session:
        match has_category:
            case MarkedInvestorEnum.RED:
                qs = get_marked_investors(
                    RMWiseRedZoneTraderORM, has_branch, has_trader
                )
            case MarkedInvestorEnum.YELLOW:
                qs = get_marked_investors(
                    RMWiseYellowZoneTraderORM, has_branch, has_trader
                )
            case _:
                # TODO: handle exception gracefully
                raise ValueError("Invalid Type")

        rows = session.execute(qs)
        results = [
            MarkedInvestor.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)
