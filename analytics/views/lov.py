from http import HTTPMethod

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from authusers.models import RoleChoices, User
from core.helper import enveloper
from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer
from db import engine

from ..models import Branch, ClusterManager, Trader
from ..orm import BranchOrm, ClusterManagerOrm, TraderOrm
from ..serializers import BranchSerializer, ClusterManagerSerializer, TraderSerializer

__all__ = [
    "get_branches",
    "get_all_traders",
    "get_traders_for_branchid",
    "get_cluster_managers",
]


@extend_schema(
    responses={200: enveloper(BranchSerializer, many=True)}, tags=[OpenApiTags.LOV]
)
@api_view([HTTPMethod.GET])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def get_branches(request: Request) -> Response:
    """fetch all branches. results will be automatically filters according to user role."""
    request.accepted_renderer = CustomRenderer()

    current_user: User = request.user

    with Session(engine) as session:
        match current_user.role:
            case RoleChoices.BRANCH_MANAGER | RoleChoices.REGIONAL_MANAGER:
                qs = session.execute(
                    select(BranchOrm)
                    .where(BranchOrm.branch_code == current_user.profile.branch_id)
                    .order_by(BranchOrm.branch_name)
                ).scalars()
            case RoleChoices.CLUSTER_MANAGER:
                join_condition = BranchOrm.branch_code == ClusterManagerOrm.branch_code
                qs = session.execute(
                    select(BranchOrm)
                    .join(ClusterManagerOrm, join_condition)
                    .where(ClusterManagerOrm.manager_name == current_user.username)
                    .order_by(BranchOrm.branch_name)
                ).scalars()
            case _:
                # management or admin
                # * Any selective type of case should be explicitly handle
                qs = session.execute(
                    select(BranchOrm).order_by(BranchOrm.branch_name)
                ).scalars()
        results = [Branch.model_validate(branch).model_dump() for branch in qs]
    return Response(results)


@extend_schema(
    responses={200: enveloper(TraderSerializer, many=True)}, tags=[OpenApiTags.LOV]
)
@api_view([HTTPMethod.GET])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def get_all_traders(request: Request) -> Request:
    """fetch all traders."""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TraderOrm).order_by(TraderOrm.branch_name)
        ).scalars()
        results = [Trader.model_validate(trader).model_dump() for trader in qs]
        return Response(results)


@extend_schema(
    operation_id="traders-with-branchId",
    responses={200: enveloper(TraderSerializer, many=True)},
    tags=[OpenApiTags.LOV],
)
@api_view([HTTPMethod.GET])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def get_traders_for_branchid(request: Request, id: int) -> Request:
    """fetch all traders respective to branchId"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        query = select(TraderOrm).order_by(TraderOrm.trader_id)
        if current_user.role == RoleChoices.REGIONAL_MANAGER:
            query = query.where(TraderOrm.trader_id == current_user.username)
        else:
            query = query.where(TraderOrm.branch_code == id)
        qs = session.execute(query).scalars()
        results = [Trader.model_validate(trader).model_dump() for trader in qs]
        return Response(results)


@extend_schema(
    responses={200: enveloper(ClusterManagerSerializer, many=True)},
    tags=[OpenApiTags.LOV],
)
@api_view([HTTPMethod.GET])
@permission_classes(
    [
        IsAuthenticated,
        IsAdminUser,
    ]
)
def get_cluster_managers(request: Request) -> Request:
    """fetch all cluster managers"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(ClusterManagerOrm).order_by(ClusterManagerOrm.branch_name)
        ).scalars()
        results = [ClusterManager.model_validate(cm).model_dump() for cm in qs]
        return Response(results)
