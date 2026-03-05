from copy import deepcopy
from datetime import datetime, timedelta
from http import HTTPMethod
from typing import Any, Dict
from urllib import response

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
     RegionalBusinessPerformance,
     RegionalOfficeSpace
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
    RegionalBusinessPerformanceORM,
    RegionalOfficeSpaceORM
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
    "get_branch_wise_regional_business_performance",
    "get_branch_wise_regional_office_space_details"
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

    #qs = rolewise_branch_data_filter(qs, current_user, ExchangeWisearketStatisticsORM)

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
    """Fetch branch-wise regional client performance/non-performance summary"""
    
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name")
    has_branch_code = request.query_params.get("branch_code")

    with Session(engine) as session:
        qs = select(
            func.sum(RegionalClientPerformanceNonPerformanceORM.total_investor).label("total_investor"),
            func.sum(RegionalClientPerformanceNonPerformanceORM.texpress_investor).label("texpress_investor"),
            func.sum(RegionalClientPerformanceNonPerformanceORM.ibroker_investor).label("ibroker_investor"),
            func.sum(RegionalClientPerformanceNonPerformanceORM.performer).label("performer"),
            func.sum(RegionalClientPerformanceNonPerformanceORM.none_performer).label("none_performer"),
            func.sum(RegionalClientPerformanceNonPerformanceORM.performer_percentage).label("performer_percentage"),
            func.sum(RegionalClientPerformanceNonPerformanceORM.nonperformer_percentage).label("nonperformer_percentage"),
        )

        # Apply role-based filters
        qs = rolewise_branch_data_filter(qs, current_user, RegionalClientPerformanceNonPerformanceORM)

        # Apply optional filters
        if has_region_name:
            qs = qs.where(RegionalClientPerformanceNonPerformanceORM.region_name == has_region_name)
        if has_branch_code:
            qs = qs.where(RegionalClientPerformanceNonPerformanceORM.branch_code == has_branch_code)

        # Fetch as a **dict-like object**
        row = session.execute(qs).mappings().first()
 
        # Validate with Pydantic
        data = RegionalClientPerformanceNonPerformance.model_validate(row).model_dump()

        return Response(data)


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
      qs = select(
           func.sum(RegionalECRMDetailsORM.total_visits).label("total_visits"),
           func.sum(RegionalECRMDetailsORM.total_success).label("total_success"),
           func.sum(RegionalECRMDetailsORM.total_in_progress).label("total_in_progress"),
           func.sum(RegionalECRMDetailsORM.total_discard).label("total_discard"),
           func.sum(RegionalECRMDetailsORM.total_existing_client_visit).label("total_existing_client_visit"),
           )

    qs = rolewise_branch_data_filter(qs, current_user, RegionalECRMDetailsORM)

    if has_region_name:
            qs = qs.where(RegionalECRMDetailsORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalECRMDetailsORM.branch_code == has_branch_code)

    rows = session.execute(qs).mappings().first()
    results = RegionalECRMDetails.model_validate(rows).model_dump()
    return Response(results)


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
      qs = select(
                   func.sum(RegionaleKYCDetailORM.total_investor).label("total_investor"),
                   func.sum(RegionaleKYCDetailORM.total_submitted).label("total_submitted"),
                   func.sum(RegionaleKYCDetailORM.due).label("due"),
                  )

    qs = rolewise_branch_data_filter(qs, current_user, RegionaleKYCDetailORM)

   
    if has_region_name:
            qs = qs.where(RegionaleKYCDetailORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionaleKYCDetailORM.branch_code == has_branch_code)

    rows = session.execute(qs).mappings().first()
    results = RegionaleKYCDetail.model_validate(rows).model_dump()
    
    return Response(results)


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
      qs = select(
                    func.sum(RegionalEmployeeStructureORM.permanent_trader).label("permanent_trader"),
                    func.sum(RegionalEmployeeStructureORM.contractual_with_salary).label("contractual_with_salary"),
                    func.sum(RegionalEmployeeStructureORM.contractual_without_salary).label("contractual_without_salary"),
                  )

    qs = rolewise_branch_data_filter(qs, current_user, RegionalEmployeeStructureORM)

   
    if has_region_name:
            qs = qs.where(RegionalEmployeeStructureORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalEmployeeStructureORM.branch_code == has_branch_code)

    rows = session.execute(qs).mappings().first()
    results = RegionalEmployeeStructure.model_validate(rows).model_dump()
    
    return Response(results)


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

    rows = session.execute(qs).scalars()
    results = [RegionalChannelWiseTrades.model_validate(row).model_dump()for row in rows ]
    
    return Response(results)


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
      qs = select(
             func.sum(RegionalPartyTurnoverCommissionORM.total_party).label("total_party"),
             func.sum(RegionalPartyTurnoverCommissionORM.total_investor).label("total_investor"),
             func.sum(RegionalPartyTurnoverCommissionORM.total_turnover).label("total_turnover"),
             func.sum(RegionalPartyTurnoverCommissionORM.total_commission).label("total_commission"),

           )

    qs = rolewise_branch_data_filter(qs, current_user, RegionalPartyTurnoverCommissionORM)
   
    if has_region_name:
            qs = qs.where(RegionalPartyTurnoverCommissionORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalPartyTurnoverCommissionORM.branch_code == has_branch_code)

    rows = session.execute(qs).mappings().first()
    results = RegionalPartyTurnoverCommission.model_validate(rows).model_dump()
    return Response(results)


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
      qs = select(
           func.sum(RegionalCashMarginDetailsORM.total_deposit).label("total_deposit"),
           func.sum(RegionalCashMarginDetailsORM.total_withdrawal).label("total_withdrawal"),
           func.sum(RegionalCashMarginDetailsORM.total_portfolio).label("total_portfolio"),
           func.sum(RegionalCashMarginDetailsORM.margin_negative).label("margin_negative"),
           func.sum(RegionalCashMarginDetailsORM.cash_available).label("cash_available"),
           )
    qs = rolewise_branch_data_filter(qs, current_user, RegionalCashMarginDetailsORM)
   
    if has_region_name:
            qs = qs.where(RegionalCashMarginDetailsORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalCashMarginDetailsORM.branch_code == has_branch_code)

    rows = session.execute(qs).mappings().first()
    results = RegionalCashMarginDetails.model_validate(rows).model_dump()
    
    return Response(results)


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
      qs = select(
           func.sum(RegionalExposureDetailsORM.ledger_bal).label("ledger_bal"),
           func.sum(RegionalExposureDetailsORM.green).label("green"),
           func.sum(RegionalExposureDetailsORM.yellow).label("yellow"),
           func.sum(RegionalExposureDetailsORM.red).label("red"),
           func.sum(RegionalExposureDetailsORM.negative_equity).label("negative_equity"),
           )
    qs = rolewise_branch_data_filter(qs, current_user, RegionalExposureDetailsORM)
   
    if has_region_name:
            qs = qs.where(RegionalExposureDetailsORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalExposureDetailsORM.branch_code == has_branch_code)

    rows = session.execute(qs).mappings().first()
    results = RegionalExposureDetails.model_validate(rows).model_dump()

    return Response(results)

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
def get_branch_wise_regional_office_space_details(request: Request) -> Response:
    """fetch branch wise regional office space details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    
    with Session(engine) as session:
      qs = select(RegionalOfficeSpaceORM).order_by(RegionalOfficeSpaceORM.branch_code)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalOfficeSpaceORM)
   
    if has_region_name:
            qs = qs.where(RegionalOfficeSpaceORM.region_name == has_region_name)
    if has_branch_code:
            qs = qs.where(RegionalOfficeSpaceORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars()
    results = [RegionalOfficeSpace.model_validate(row).model_dump()for row in rows ]

    return Response(results)