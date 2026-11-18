from http import HTTPMethod

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from sqlalchemy import   select
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
     RegionalOfficeSpace,
     RegionalPerformanceProcess,
     AdminRegionalManagerRMBusinessperformance
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
    RegionalOfficeSpaceORM,
    RegionalPerformanceProcessORM,
    AdminRegionalManagerRMBusinessperformanceORM
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
    "get_branch_wise_regional_office_space_details",
    "get_branch_performance_process_details",
    "get_admin_regional_manager_rm_business_performance"
]



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

    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_market_statistics(request: Request) -> Response:
    """fetch branch wise market statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
      qs = select(BranchWisearketStatisticsORM).order_by(BranchWisearketStatisticsORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, BranchWisearketStatisticsORM)


    rows = session.execute(qs).scalars()
    results = [BranchWisearketStatistics.model_validate(row).model_dump()for row in rows ]

    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_client_performance_nonperformance_list(request: Request) -> Response:
    """Fetch branch-wise regional client performance/non-performance summary"""
    
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user


    with Session(engine) as session:
        qs = select(RegionalClientPerformanceNonPerformanceORM).order_by(RegionalClientPerformanceNonPerformanceORM.branch_code)

        # Apply role-based filters
        qs = rolewise_branch_data_filter(qs, current_user, RegionalClientPerformanceNonPerformanceORM)

        # Fetch as a **dict-like object**
        rows = session.execute(qs).scalars()
        results = [RegionalClientPerformanceNonPerformance.model_validate(row).model_dump()for row in rows ]

        return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_eCRM_details_list(request: Request) -> Response:
    """fetch branch wise regional eCRM details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    
    with Session(engine) as session:
      qs = select(RegionalECRMDetailsORM).order_by(RegionalECRMDetailsORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, RegionalECRMDetailsORM)

   

    rows = session.execute(qs).scalars()
    results = [RegionalECRMDetails.model_validate(row).model_dump()for row in rows ]
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP]
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_eKYC_details_list(request: Request) -> Response:
    """fetch branch wise regional eKYC details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    
    with Session(engine) as session:
      qs = select(RegionaleKYCDetailORM).order_by(RegionaleKYCDetailORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, RegionaleKYCDetailORM)


    rows = session.execute(qs).scalars()
    results = [RegionaleKYCDetail.model_validate(row).model_dump()for row in rows ]
    
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_employee_structure_list(request: Request) -> Response:
    """fetch branch wise regional employee structure statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    
    with Session(engine) as session:
      qs = select(RegionalEmployeeStructureORM).order_by(RegionalEmployeeStructureORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, RegionalEmployeeStructureORM)


    rows = session.execute(qs).scalars()
    results = [RegionalEmployeeStructure.model_validate(row).model_dump()for row in rows ]
    
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_channel_wise_trades_list(request: Request) -> Response:
    """fetch branch wise regional channel wise trades statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    
    with Session(engine) as session:
      qs = select(RegionalChannelWiseTradesORM)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalChannelWiseTradesORM)
   
    rows = session.execute(qs).scalars()
    results = [RegionalChannelWiseTrades.model_validate(row).model_dump()for row in rows ]
    
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_party_wise_turnover_commission(request: Request) -> Response:
    """fetch branch wise regional party wise turnover commission statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    
    with Session(engine) as session:
      qs = select(RegionalPartyTurnoverCommissionORM).order_by(RegionalPartyTurnoverCommissionORM.branch_code)

    qs = rolewise_branch_data_filter(qs, current_user, RegionalPartyTurnoverCommissionORM)


    rows = session.execute(qs).scalars()
    results = [RegionalPartyTurnoverCommission.model_validate(row).model_dump()for row in  rows ]
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP]
    )
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_deposit_withdraw_details(request: Request) -> Response:
    """fetch branch wise regional deposit and withdrawal details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user
    
    with Session(engine) as session:
      qs = select(RegionalCashMarginDetailsORM).order_by(RegionalCashMarginDetailsORM.branch_code)
          
    qs = rolewise_branch_data_filter(qs, current_user, RegionalCashMarginDetailsORM)


    rows = session.execute(qs).scalars()
    results = [RegionalCashMarginDetails.model_validate(row).model_dump()for row in rows ]
    
    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_exposure_details(request: Request) -> Response:
    """fetch branch wise regional exposure details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
      qs = select(RegionalExposureDetailsORM).order_by(RegionalExposureDetailsORM.branch_code)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalExposureDetailsORM)
   
  

    rows = session.execute(qs).scalars()
    results = [RegionalExposureDetails.model_validate(row).model_dump()for row in rows ]

    return Response(results)

@extend_schema(
    tags=[OpenApiTags.RBP]
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_business_performance(request: Request) -> Response:
    """fetch branch wise regional business performance statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
      qs = select(RegionalBusinessPerformanceORM).order_by(RegionalBusinessPerformanceORM.branch_code)
      qs = rolewise_branch_data_filter(qs, current_user, RegionalBusinessPerformanceORM)
   
  

    rows = session.execute(qs).scalars()
    results = [RegionalBusinessPerformance.model_validate(row).model_dump()for row in rows ]
    
    return Response(results)



@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_wise_regional_office_space_details(request: Request) -> Response:
    """fetch branch wise regional office space details statistics"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    
    with Session(engine) as session:
      qs = select(RegionalOfficeSpaceORM).order_by(RegionalOfficeSpaceORM.branch_code)
    qs = rolewise_branch_data_filter(qs, current_user, RegionalOfficeSpaceORM)


    rows = session.execute(qs).scalars()
    results = [RegionalOfficeSpace.model_validate(row).model_dump()for row in rows ]

    return Response(results)


@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_branch_performance_process_details(request: Request) -> Response:
    """fetch branch performance process details like last execution time, parameters used etc."""

    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    with Session(engine) as session:
        qs = (
            select(RegionalPerformanceProcessORM)
        )

        ## qs = rolewise_branch_data_filter(qs, current_user, RegionalPerformanceProcessORM)

        row = session.execute(qs).scalar_one_or_none()

        result = RegionalPerformanceProcess.model_validate(row).model_dump()

    return Response(result)


@extend_schema(
    tags=[OpenApiTags.RBP],
)
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated])
def get_admin_regional_manager_rm_business_performance(request: Request) -> Response:
    """fetch branch wise regional business performance details for admin and regional manager"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    
    with Session(engine) as session:
      qs = select(AdminRegionalManagerRMBusinessperformanceORM).order_by(AdminRegionalManagerRMBusinessperformanceORM.trader_id)
    qs = rolewise_branch_data_filter(qs, current_user, AdminRegionalManagerRMBusinessperformanceORM)


    rows = session.execute(qs).scalars()
    results = [AdminRegionalManagerRMBusinessperformance.model_validate(row).model_dump()for row in rows ]

    return Response(results)

