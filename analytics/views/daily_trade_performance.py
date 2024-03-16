from http import HTTPMethod

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from authusers.models import User
from core.renderer import CustomRenderer
from db import engine

from ..orm import OverallSummaryOrm

__all__ = ["get_basic_summaries", "get_basic_summaries_by_branchid"]


@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_basic_summaries(request: Request) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    with Session(engine) as session:
        qs = session.execute(
            select(
                func.sum(OverallSummaryOrm.total_client).label("total_clients"),
                func.sum(OverallSummaryOrm.total_active_client).label(
                    "total_active_clients"
                ),
            )
        ).scalars()

        from devtools import debug

        debug(qs.all())
    return Response({"user": current_user.username})


@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_basic_summaries_by_branchid(request: Request, branch_id: int) -> Response:
    """fetch basic branch summary"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    return Response({"user": current_user.__dict__, "branch_id": branch_id})
