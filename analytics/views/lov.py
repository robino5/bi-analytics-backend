from http import HTTPMethod
from typing import List

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.renderer import CustomRenderer
from db import engine

from ..models import Branch, ClusterManager, Trader
from ..orm import BranchOrm, ClusterManagerOrm, TraderOrm


@api_view([HTTPMethod.GET])
def get_branches(request: Request) -> Response:
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(BranchOrm).order_by(BranchOrm.branch_name)
        ).scalars()
        results = [Branch.model_validate(branch).model_dump() for branch in qs]
    return Response(results)


@api_view([HTTPMethod.GET])
def get_all_traders(request: Request) -> Request:
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TraderOrm).order_by(TraderOrm.branch_name)
        ).scalars()
        results = [Trader.model_validate(trader).model_dump() for trader in qs]
        return Response(results)


@extend_schema(
    operation_id="traders-with-branchId",
    responses=List[Trader],
)
@api_view([HTTPMethod.GET])
def get_traders_for_branchcode(request: Request, id: int) -> Request:
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(TraderOrm)
            .where(TraderOrm.branch_code == id)
            .order_by(TraderOrm.branch_name)
        ).scalars()
        results = [Trader.model_validate(trader).model_dump() for trader in qs]
        return Response(results)


@extend_schema(
    responses=List[ClusterManager],
)
@api_view([HTTPMethod.GET])
def get_cluster_managers(request: Request) -> Request:
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(ClusterManagerOrm).order_by(ClusterManagerOrm.branch_name)
        ).scalars()
        results = [ClusterManager.model_validate(cm).model_dump() for cm in qs]
        return Response(results)
