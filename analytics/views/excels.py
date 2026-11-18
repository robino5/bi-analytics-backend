from http import HTTPMethod
from sqlalchemy import select
from sqlalchemy.orm import Session
from analytics.views.utils import generate_csv
from db import engine
from datetime import datetime
from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view, permission_classes

from core.metadata.openapi.configs import OpenApiTags

from rest_framework.permissions import IsAuthenticated
from core.permissions import IsManagementUser

from authusers.models import User
from core.renderer import CustomRenderer

from ..models import (
    AdminOMSBranchWiseTurnoverAsOnMonth,
    AdminOMSBranchWiseTurnoverDtAsOnMonth,
    RegionalBusinessPerformance,
    MarketRiskData
)
from ..orm import (
    AdminOMSBranchWiseTurnoverAsOnMonthORM,
    AdminOMSBranchWiseTurnoverDtAsOnMonthORM,
    RegionalBusinessPerformanceORM,
    MarketRiskDataORM
)

__all__ = [
    "download_admin_oms_datewise_turnover_csv",
    "download_admin_oms_datewise_dt_turnover_csv",
    "download_regional_business_performance_csv",
    "download_admin_market_risk_data_csv"
]


@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
def download_admin_oms_datewise_turnover_csv(request):
    """Download admin OMS Branch wise turnover as CSV"""
    with Session(engine) as session:
        qs = session.execute(
            select(AdminOMSBranchWiseTurnoverAsOnMonthORM).order_by(
                AdminOMSBranchWiseTurnoverAsOnMonthORM.branch_Name
            )
        ).scalars()

        results = [AdminOMSBranchWiseTurnoverAsOnMonth.model_validate(row).model_dump() for row in qs]
        
    header_mapping = {
        "branch_Name": "Branch Name",
        "active_clients_today": "Active Clients Today",
        "turnover_today": "Turnover Today",
        "active_clients_month": f"Active Clients-{datetime.now().strftime("%B-%Y")}",
        "turnover_month": f"Turnover-{datetime.now().strftime("%B-%Y")}"
    }
    headers = list(header_mapping.values())
    remapped_results = [
        {header_mapping[key]: value for key, value in row.items() if key in header_mapping}
        for row in results
    ]
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"branchwise_turnover-internet-{current_time}"
    return generate_csv(remapped_results, headers, filename)
    

@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
def download_admin_oms_datewise_dt_turnover_csv(request):
    """Download admin OMS Branch wise dt turnover as CSV"""
    with Session(engine) as session:
        qs = session.execute(
            select(AdminOMSBranchWiseTurnoverDtAsOnMonthORM).order_by(
                AdminOMSBranchWiseTurnoverDtAsOnMonthORM.branch_Name
            )
        ).scalars()

        results = [AdminOMSBranchWiseTurnoverDtAsOnMonth.model_validate(row).model_dump() for row in qs]
        
    header_mapping = {
        "branch_Name": "Branch Name",
        "active_clients_today": "Active Clients Today",
        "turnover_today": "Turnover Today",
        "active_clients_month": f"Active Clients-{datetime.now().strftime("%B-%Y")}",
        "turnover_month": f"Turnover-{datetime.now().strftime("%B-%Y")}"
    }
    headers = list(header_mapping.values())
    remapped_results = [
        {header_mapping[key]: value for key, value in row.items() if key in header_mapping}
        for row in results
    ]
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"branchwise_turnover-dt-{current_time}"
    return generate_csv(remapped_results, headers, filename)

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
def download_regional_business_performance_csv(request):
    """Download regional business performance as CSV"""
    request.accepted_renderer = CustomRenderer()
    current_user: User = request.user

    has_region_name = request.query_params.get("region_name", None)
    has_branch_code = request.query_params.get("branch_code", None)
    with Session(engine) as session:
        with Session(engine) as session:
         qs = select(RegionalBusinessPerformanceORM).order_by(RegionalBusinessPerformanceORM.branch_code)

        if has_region_name:
            qs = qs.where(RegionalBusinessPerformanceORM.region_name == has_region_name)
        if has_branch_code:
            qs = qs.where(RegionalBusinessPerformanceORM.branch_code == has_branch_code)

    rows = session.execute(qs).scalars()
    results = [RegionalBusinessPerformance.model_validate(row).model_dump()for row in rows ]
        
    header_mapping = {
        "branch_name": "Branch Name",
        "target": " Turnover Target",
        "turnover_achieved": "Turnover Achieved",
        "turnover_percentage": "Turnover Percentage",
        "fund_target": "Fund Target",
        "total_net_fund": "Total Net Fund",
        "total_net_link_share": "Total Net Link Share",
        "fund_percentage": "Fund Percentage",
        "bo_opening_target": "BO Opening Target",
        "bo_opened": "BO Opened",
        "bo_percentage": "BO Percentage",
        "total_trade_days": "Total Trade Days",
        "commission": "Commission",
        "total_link_share_in": "Total Link Share In",
        "total_link_share_out": "Total Link Share Out",
        "total_deposit": "Total Deposit",
        "total_withdrawal": "Total Withdrawal",
        "total_expenses": "Total Expenses",
        "profit_loss": "Profit/Loss"
    }
    headers = list(header_mapping.values())
    remapped_results = [
        {header_mapping[key]: value for key, value in row.items() if key in header_mapping}
        for row in results
    ]
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"business_performance-{current_time}"
    return generate_csv(remapped_results, headers, filename)

@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
def download_admin_market_risk_data_csv(request):
    """Download admin market risk data as CSV"""
    with Session(engine) as session:
        qs = session.execute(select(MarketRiskDataORM)).scalars()

        results = [MarketRiskData.model_validate(row).model_dump() for row in qs]
        
    header_mapping = {
        "symbol": "Symbol",
        "risk_level": "Risk Level",
        "lbs_free_float_salable": "LBS Free Float Salable",
        "single_scrip_bar": "Single Scrip Bar (%)",
        "buy_qty": "Buy Quantity",
        "sell_qty": "Sell Quantity",
        "block_pb_contact_today": "Block PB Contact Today",
        "holding_live": "Holding Live",
        "free_float_salable": "Free Float Salable",
        "sector_name": "Sector Name",
        "market_category": "Market Category",
        "dse_30": "DSE 30",
        "m_loan_listed": "M Loan Listed",
        "lbs_holding_percent": "LBS Holding Percentage",
        "margin_qty_percentage": "Margin Quantity Percentage",
        "third_party_percentage": "Third Party Percentage",
        "in_house_transaction": "In-House Transaction"
    }

    headers = list(header_mapping.values())
    remapped_results = [
        {header_mapping[key]: value for key, value in row.items() if key in header_mapping}
        for row in results
    ]
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"market_risk_data-{current_time}"
    return generate_csv(remapped_results, headers, filename)

   

