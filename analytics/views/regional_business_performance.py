from copy import deepcopy
from datetime import datetime, timedelta
from http import HTTPMethod
from typing import Any, Dict

import pandas as pd
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import Sequence, func, select
from sqlalchemy.orm import Session

from analytics.views.utils import rolewise_branch_data_filter
from authusers.models import User
from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer
from db import engine

from ..models import (
     BranchWisearketStatistics,
     ExchangeWisearketStatistics,
     RegionalClientPerformanceNonPerformance,
     RegionalECRMDetails,RegionaleKYCDetail,
     RegionalEmployeeStructure,
     RegionalChannelWiseTrades,
     RegionalPartyTurnoverCommission,
     RegionalCashMarginDetails,
     RegionalExposureDetails,
     RegionalBusinessPerformance
     )

from ..orm import (
    ExchangeWisearketStatisticsORM,
    BranchWisearketStatisticsORM,
    RegionalClientPerformanceNonPerformanceORM,
    RegionalECRMDetailsORM, 
    RegionaleKYCDetailORM,
    RegionalEmployeeStructureORM,
    RegionalChannelWiseTradesORM,
    RegionalPartyTurnoverCommissionORM,
    RegionalCashMarginDetailsORM,
    RegionalExposureDetailsORM,
    RegionalBusinessPerformanceORM
)

__all__ = [
    "get_exchange_wise_market_statistics",
    "get_branch_wise_market_statistics",
    "get_branch_wise_regional_client_performance_nonperformance_list",
    "get_branch_wise_regional_eKYC_details_list",
    "get_branch_wise_regional_eCRM_details_list",
    "get_branch_wise_regional_employee_structure_list",
    "get_branch_wise_regional_channel_wise_trades_list",
    "get_branch_wise_regional_party_wise_turnover_commission",
    "get_branch_wise_regional_deposit_withdraw_details",
    "get_branch_wise_regional_exposure_details",
    "get_branch_wise_regional_business_performance"
]


def get_sum_of_property(property: str, rows: Sequence[Dict[str, Any]]) -> int:
    sum = 0
    for row in rows:
        sum += row.get(property, 0)
    return round(sum)

@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "exchange",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific exchange",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_exchange_wise_market_statistics(request: Request) -> Response:
    """fetch exchange wise market statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_exchange = request.query_params.get("exchange", None)
    
    with Session(engine) as session:
      qs = select(ExchangeWisearketStatisticsORM).order_by(ExchangeWisearketStatisticsORM.exchange)

    qs = rolewise_branch_data_filter(qs, current_user, ExchangeWisearketStatisticsORM)

    if has_exchange:
            qs = qs.where(ExchangeWisearketStatisticsORM.exchange == has_exchange)

    rows = session.execute(qs).scalars()
    results = [ExchangeWisearketStatistics.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_turnover": get_sum_of_property('total_turnover', results),
            "sum_of_avg_turnover": get_sum_of_property('avg_turnover', results),
            "sum_of_lbsl_total_turnover": get_sum_of_property('lbsl_total_turnover', results),
            "sum_of_lbsl_avg_turnover": get_sum_of_property('lbsl_avg_turnover', results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_market_statistics(request: Request) -> Response:
    """fetch branch wise market statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(BranchWisearketStatisticsORM).order_by(BranchWisearketStatisticsORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, BranchWisearketStatisticsORM)

   
    if has_region_name:
            qs = qs.where(BranchWisearketStatisticsORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(BranchWisearketStatisticsORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars()
    results = [BranchWisearketStatistics.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_turnover": get_sum_of_property('total_turnover', results),
            "sum_of_avg_turnover": get_sum_of_property('avg_turnover', results)
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_client_performance_nonperformance_list(request: Request) -> Response:
    """fetch branch wise regional client performance nonperformance statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalClientPerformanceNonPerformanceORM).order_by(RegionalClientPerformanceNonPerformanceORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, RegionalClientPerformanceNonPerformanceORM)

   
    if has_region_name:
            qs = qs.where(RegionalClientPerformanceNonPerformanceORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalClientPerformanceNonPerformanceORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars()
    results = [RegionalClientPerformanceNonPerformance.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_investor": get_sum_of_property('total_investor', results),
            "sum_of_texpress_investor": get_sum_of_property('texpress_investor', results),
            "sum_of_ibroker_investor": get_sum_of_property('ibroker_investor', results),
            "sum_of_performer": get_sum_of_property('performer', results),
            "sum_of_none_performer": get_sum_of_property('none_performer', results),
            "sum_of_performer_percentage": get_sum_of_property('performer_percentage', results),
            "sum_of_nonperformer_percentage": get_sum_of_property('nonperformer_percentage', results)
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_eCRM_details_list(request: Request) -> Response:
    """fetch branch wise regional eCRM details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalECRMDetailsORM).order_by(RegionalECRMDetailsORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, RegionalECRMDetailsORM)

   
    if has_region_name:
            qs = qs.where(RegionalECRMDetailsORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalECRMDetailsORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars()
    results = [RegionalECRMDetails.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_visits": get_sum_of_property('total_visits', results),
            "sum_of_total_success": get_sum_of_property('total_success', results),
            "sum_of_total_in_progress": get_sum_of_property('total_in_progress', results),
            "sum_of_total_discard": get_sum_of_property('total_discard', results),
            "sum_of_total_existing_client_visit": get_sum_of_property('total_existing_client_visit', results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_eKYC_details_list(request: Request) -> Response:
    """fetch branch wise regional eKYC details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionaleKYCDetailORM).order_by(RegionaleKYCDetailORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, RegionaleKYCDetailORM)

   
    if has_region_name:
            qs = qs.where(RegionaleKYCDetailORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionaleKYCDetailORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars()
    results = [RegionaleKYCDetail.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_investor": get_sum_of_property('total_investor', results),
            "sum_of_total_submitted": get_sum_of_property('total_submitted', results),
            "sum_of_due": get_sum_of_property('due', results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_employee_structure_list(request: Request) -> Response:
    """fetch branch wise regional employee structure statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalEmployeeStructureORM).order_by(RegionalEmployeeStructureORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, RegionalEmployeeStructureORM)

   
    if has_region_name:
            qs = qs.where(RegionalEmployeeStructureORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalEmployeeStructureORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars()
    results = [RegionalEmployeeStructure.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_permanent_trader": get_sum_of_property('permanent_trader', results),
            "sum_of_contractual_with_salary": get_sum_of_property('contractual_with_salary', results),
            "sum_of_contractual_without_salary": get_sum_of_property('contractual_without_salary', results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_channel_wise_trades_list(request: Request) -> Response:
    """fetch branch wise regional channel wise trades statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalChannelWiseTradesORM)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalChannelWiseTradesORM)
   
    if has_region_name:
            qs = qs.where(RegionalChannelWiseTradesORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalChannelWiseTradesORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars().all()
    results = [RegionalChannelWiseTrades.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_clients": get_sum_of_property('total_clients', results),
            "sum_of_total_trades": get_sum_of_property('total_trades', results),
            "sum_of_total_turnover": get_sum_of_property('total_turnover', results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_party_wise_turnover_commission(request: Request) -> Response:
    """fetch branch wise regional party wise turnover commission statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalPartyTurnoverCommissionORM)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalPartyTurnoverCommissionORM)
   
    if has_region_name:
            qs = qs.where(RegionalPartyTurnoverCommissionORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalPartyTurnoverCommissionORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars().all()
    results = [RegionalPartyTurnoverCommission.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_party": get_sum_of_property('total_party', results),
            "sum_of_total_investor": get_sum_of_property('total_investor', results),
            "sum_of_total_turnover": get_sum_of_property('total_turnover', results),
            "sum_of_total_commission": get_sum_of_property('total_commission', results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_deposit_withdraw_details(request: Request) -> Response:
    """fetch branch wise regional deposit and withdrawal details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalCashMarginDetailsORM)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalCashMarginDetailsORM)
   
    if has_region_name:
            qs = qs.where(RegionalCashMarginDetailsORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalCashMarginDetailsORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars().all()
    results = [RegionalCashMarginDetails.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_deposit": get_sum_of_property('total_deposit', results),
            "sum_of_total_withdrawal": get_sum_of_property('total_withdrawal', results),
            "sum_of_total_portfolio": get_sum_of_property('total_portfolio', results),
            "sum_of_margin_negative": get_sum_of_property('margin_negative', results),
            "sum_of_cash_available": get_sum_of_property('cash_available', results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_exposure_details(request: Request) -> Response:
    """fetch branch wise regional exposure details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalExposureDetailsORM)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalExposureDetailsORM)
   
    if has_region_name:
            qs = qs.where(RegionalExposureDetailsORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalExposureDetailsORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars().all()
    results = [RegionalExposureDetails.model_validate(row).model_dump()for row in rows ]
    
    response = {
        "detail": {
            "sum_of_total_ledger_bal": get_sum_of_property('ledger_bal', results),
            "sum_of_total_green": get_sum_of_property('green', results),
            "sum_of_total_yellow": get_sum_of_property('yellow', results),
            "sum_of_margin_red": get_sum_of_property('red', results),
            "sum_of_negative_equity": get_sum_of_property('negative_equity', results),
        },
        "rows": results,
    }
    return Response(response)


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "region_name",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific region name",
        ),
           OpenApiParameter(
            "branch_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=False,
            description="get results with specific branch code",
        ),
    ],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_business_performance(request: Request) -> Response:
    """fetch branch wise regional business performance statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalBusinessPerformanceORM).order_by(RegionalBusinessPerformanceORM.branch_code)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalBusinessPerformanceORM)
   
    if has_region_name:
            qs = qs.where(RegionalBusinessPerformanceORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalBusinessPerformanceORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars()
    results = [RegionalBusinessPerformance.model_validate(row).model_dump()for row in rows ]
    
    # response = {
    #     "detail": {
    #         "sum_of_total_ledger_bal": get_sum_of_property('ledger_bal', results),
    #         "sum_of_total_green": get_sum_of_property('green', results),
    #         "sum_of_total_yellow": get_sum_of_property('yellow', results),
    #         "sum_of_margin_red": get_sum_of_property('red', results),
    #         "sum_of_negative_equity": get_sum_of_property('negative_equity', results),
    #     },
    #     "rows": results,
    # }
    return Response(results)