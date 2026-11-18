from http import HTTPMethod
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import  select
from sqlalchemy.orm import Session
from drf_spectacular.utils import  extend_schema


from core.metadata.openapi import OpenApiTags
from core.permissions import IsManagementUser
from core.renderer import CustomRenderer
from db import engine

from ..models import (
MarketSpotDataInvestorDrillDown
)
from ..orm import (
   MarketSpotDataInvestorDrillDownORM
)

__all__ = [
  "get_marketSpotDataInvestorDrillDown"
]

@extend_schema(tags=[OpenApiTags.TRADE_INSIGHTS])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_marketSpotDataInvestorDrillDown(request: Request) -> Response:
    """fetch market spot data for investor drilldown"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(MarketSpotDataInvestorDrillDownORM)
        ).scalars()

        results = [MarketSpotDataInvestorDrillDown.model_validate(row).model_dump() for row in qs]

    return Response(results)