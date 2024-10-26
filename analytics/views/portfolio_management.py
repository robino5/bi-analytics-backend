from copy import deepcopy
from datetime import datetime, timedelta
from http import HTTPMethod

import pandas as pd
from drf_spectacular.utils import extend_schema
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

from ..models import DailyNetFundFlow, PortfolioStatus, TradeVsClient
from ..orm import (
    AccountOpeningFundInOutFlowOrm,
    DailyNetFundFlowOrm,
    PortfolioManagementStatusOrm,
    TurnoverAndClientsTradeOrm,
    TurnoverPerformanceOrm,
)
from .utils import rolewise_branch_data_filter

__all__ = [
    "get_daily_net_fundflow",
    "get_daily_net_fundflow_by_branchid",
    "get_trade_vs_client_statistics",
    "get_trade_vs_client_statistics_by_branchid",
    "get_turnover_performance",
    "get_turnover_performance_by_branchid",
    "get_accounts_fundflow",
    "get_accounts_fundflow_by_branchid",
    "get_portfolio_status",
    "get_portfolio_status_by_branchid",
]


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_daily_net_fundflow(request: Request) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    threshold_date = datetime.now() - timedelta(days=120)

    with Session(engine) as session:
        qs = (
            select(
                DailyNetFundFlowOrm.trading_date.label("trading_date"),
                func.sum(DailyNetFundFlowOrm.fundflow).label("amount"),
            )
            .where(DailyNetFundFlowOrm.trading_date >= threshold_date)
            .group_by(DailyNetFundFlowOrm.trading_date)
        )

        qs = rolewise_branch_data_filter(qs, current_user, DailyNetFundFlowOrm)
        rows = session.execute(qs)
        results = [
            DailyNetFundFlow.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_daily_net_fundflow_by_branchid(request: Request, id: int) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                DailyNetFundFlowOrm.trading_date.label("trading_date"),
                func.sum(DailyNetFundFlowOrm.fundflow).label("amount"),
            )
            .where(DailyNetFundFlowOrm.branch_code == id)
            .group_by(DailyNetFundFlowOrm.trading_date)
        )

        rows = session.execute(qs)
        results = [
            DailyNetFundFlow.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_trade_vs_client_statistics(request: Request) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    threshold_date = datetime.now() - timedelta(days=120)

    with Session(engine) as session:
        qs = (
            select(
                TurnoverAndClientsTradeOrm.trading_date.label("trading_date"),
                func.sum(TurnoverAndClientsTradeOrm.turnover).label("turnover"),
                func.sum(TurnoverAndClientsTradeOrm.active_client).label(
                    "active_clients"
                ),
            )
            .where(TurnoverAndClientsTradeOrm.trading_date >= threshold_date)
            .group_by(TurnoverAndClientsTradeOrm.trading_date)
        )

        qs = rolewise_branch_data_filter(qs, current_user, TurnoverAndClientsTradeOrm)

        rows = session.execute(qs)
        results = [
            TradeVsClient.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_trade_vs_client_statistics_by_branchid(request: Request, id: int) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = (
            select(
                TurnoverAndClientsTradeOrm.trading_date.label("trading_date"),
                func.sum(TurnoverAndClientsTradeOrm.turnover).label("turnover"),
                func.sum(TurnoverAndClientsTradeOrm.active_client).label(
                    "active_clients"
                ),
            )
            .where(TurnoverAndClientsTradeOrm.branch_code == id)
            .group_by(TurnoverAndClientsTradeOrm.trading_date)
        )

        rows = session.execute(qs)
        results = [
            TradeVsClient.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_turnover_performance(request: Request, *args, **kwargs) -> Response:
    """fetch summary of turnover performance"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = select(
            TurnoverPerformanceOrm.branch_code,
            TurnoverPerformanceOrm.branch_name,
            TurnoverPerformanceOrm.col1,
            TurnoverPerformanceOrm.col2,
            TurnoverPerformanceOrm.col3,
        )

        qs = rolewise_branch_data_filter(qs, current_user, TurnoverPerformanceOrm)

        rows = session.execute(qs)

        df = pd.DataFrame([row._asdict() for row in rows], columns=rows.keys())
        df["col2"] = df["col2"].str.strip()  # trim the col2, has space

        df = df[df["col2"] != "3.Achieved Turnover (times of target)"]

        pivot_df = df.pivot_table(
            index="col2", columns="col3", values="col1", aggfunc="sum"
        ).reset_index()  # aggregate the df

        pivot_df.columns = map(str.lower, pivot_df.columns)

        pivot_df.rename(columns={"col2": "name"}, inplace=True)
        data = pivot_df.to_dict(orient="records")

        _target_sums = deepcopy(data[0])
        _generated_sums = deepcopy(data[-1])
        _target_sums.pop("name")
        _generated_sums.pop("name")
        data.append({"name": "3.Achieved Turnover (times of target)"})
        for key, val in _target_sums.items():
            data[-1][key] = f"{(_generated_sums.get(key) / val):.2f}"
    return Response(data)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_turnover_performance_by_branchid(request: Request, id: int) -> Response:
    """fetch summary of turnover performance"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        query = select(
            TurnoverPerformanceOrm.branch_code,
            TurnoverPerformanceOrm.branch_name,
            TurnoverPerformanceOrm.col1,
            TurnoverPerformanceOrm.col2,
            TurnoverPerformanceOrm.col3,
        ).where(TurnoverPerformanceOrm.branch_code == id)
        rows = session.execute(query)

        df = pd.DataFrame([row._asdict() for row in rows], columns=rows.keys())
        df["col2"] = df["col2"].str.strip()  # trim the col2, has space

        pivot_df = df.pivot_table(
            index="col2", columns="col3", values="col1", aggfunc="sum"
        ).reset_index()  # aggregate the df

        pivot_df.columns = map(str.lower, pivot_df.columns)

        pivot_df.rename(
            columns={
                "col2": "name",
            },
            inplace=True,
        )
    return Response(pivot_df.to_dict(orient="records"))


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_accounts_fundflow(request: Request) -> Response:
    """fetch account and fundflow overview"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = select(
            AccountOpeningFundInOutFlowOrm.branch_code,
            AccountOpeningFundInOutFlowOrm.branch_name,
            AccountOpeningFundInOutFlowOrm.col1,
            AccountOpeningFundInOutFlowOrm.col2,
            AccountOpeningFundInOutFlowOrm.col3,
        )

        qs = rolewise_branch_data_filter(
            qs, current_user, AccountOpeningFundInOutFlowOrm
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


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_accounts_fundflow_by_branchid(request: Request, id: int) -> Response:
    """fetch account and fundflow overview"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        query = select(
            AccountOpeningFundInOutFlowOrm.branch_code,
            AccountOpeningFundInOutFlowOrm.branch_name,
            AccountOpeningFundInOutFlowOrm.col1,
            AccountOpeningFundInOutFlowOrm.col2,
            AccountOpeningFundInOutFlowOrm.col3,
        ).where(AccountOpeningFundInOutFlowOrm.branch_code == id)
        rows = session.execute(query)

        df = pd.DataFrame([row._asdict() for row in rows], columns=rows.keys())
        df["col2"] = df["col2"].str.strip()  # trim the col2, has space

        pivot_df = df.pivot_table(
            index="col2", columns="col3", values="col1", aggfunc="sum"
        ).reset_index()  # aggregate the df

        pivot_df.columns = map(str.lower, pivot_df.columns)

        pivot_df.rename(columns={"col2": "name"}, inplace=True)
    return Response(pivot_df.to_dict(orient="records"))


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_portfolio_status(request: Request) -> Response:
    """fetch portfolio management status overview"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = (
            select(
                PortfolioManagementStatusOrm.perticular,
                func.sum(PortfolioManagementStatusOrm.amount).label("amount"),
            )
            .group_by(PortfolioManagementStatusOrm.perticular)
            .order_by(PortfolioManagementStatusOrm.perticular)
        )

        qs = rolewise_branch_data_filter(qs, current_user, PortfolioManagementStatusOrm)

        rows = session.execute(qs)
        results = [
            PortfolioStatus.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)


@extend_schema(tags=[OpenApiTags.PM])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_portfolio_status_by_branchid(request: Request, id: int) -> Response:
    """fetch portfolio management status overview"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        query = (
            select(
                PortfolioManagementStatusOrm.perticular,
                func.sum(PortfolioManagementStatusOrm.amount).label("amount"),
            )
            .where(PortfolioManagementStatusOrm.branch_code == id)
            .group_by(PortfolioManagementStatusOrm.perticular)
            .order_by(PortfolioManagementStatusOrm.perticular)
        )
        rows = session.execute(query)
        results = [
            PortfolioStatus.model_validate(row._asdict()).model_dump() for row in rows
        ]
    return Response(results)
