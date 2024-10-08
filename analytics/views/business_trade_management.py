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

from ..models import BoardTurnOver, BoardTurnOverBreakdown
from ..orm import BoardTurnOverBreakdownOrm, BoardTurnOverOrm


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_board_turnovers(request: Request) -> Response:
    """fetch branch turnovers"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(BoardTurnOverOrm).order_by(
                BoardTurnOverOrm.board
            )
        ).scalars()

        results = [BoardTurnOver.model_validate(row).model_dump() for row in qs]

    return Response(results)


@extend_schema(tags=[OpenApiTags.BUSINESS_TRADE_MANAGEMENT])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, ExtendedIsAdminUser])
def get_board_turnovers_breakdown(request: Request) -> Response:
    """fetch branch turnovers"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(BoardTurnOverBreakdownOrm).order_by(
                BoardTurnOverBreakdownOrm.board
            )
        ).scalars()

        results = [BoardTurnOverBreakdown.model_validate(row).model_dump() for row in qs]

    return Response(results)
