from http import HTTPMethod
from datetime import datetime
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
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
MarketSpotDataInvestorDrillDown,
MarketZGroupDataInvestorDrillDown
)
from ..orm import (
   MarketSpotDataInvestorDrillDownORM,
   MarketZGroupDataInvestorDrillDownORM
)
from .utils import generate_csv

__all__ = [
  "get_marketSpotDataInvestorDrillDown",
  "get_marketSpotDataInvestorDrillDowncsv",
  "get_marketZGroupDataInvestorDrillDown",
  "get_marketZGroupDataInvestorDrillDowncsv"
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


@extend_schema(tags=[OpenApiTags.TRADE_INSIGHTS])
@api_view([HTTPMethod.GET])
@permission_classes([AllowAny])
def get_marketSpotDataInvestorDrillDowncsv(request: Request) -> Response:
    """fetch market spot data for investor drilldown as CSV"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(MarketSpotDataInvestorDrillDownORM)
        ).scalars()

        results = [MarketSpotDataInvestorDrillDown.model_validate(row).model_dump() for row in qs]

        header_mapping = {
            "symbol": "Symbol",
            "investor_code": "Investor Code",
            "investor_name": "Investor Name",
            "account_type": "Account Type",
            "current_balance": "Current Balance",
            "ledger_balance": "Ledger Balance",
            "spot_buy_qty": "Spot Buy Quantity",
            "spot_buy_amount": "Spot Buy Amount",
            "cash_deposit": "Cash Deposit",
            "non_cash_deposit": "Non-Cash Deposit",
            "used_excess_lbsl_fund": "Used Excess LBSL Fund",
            "fund_using_level": "Fund Using Level",
            "rm_branch": "RM Branch",
            "rm_name": "RM Name",
        }
        remapped_results = [
            {header: row.get(field) for field, header in header_mapping.items()}
            for row in results
        ]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"market_spot_investor_drilldown-{timestamp}"
        return generate_csv(remapped_results, list(header_mapping.values()), filename)

@extend_schema(tags=[OpenApiTags.TRADE_INSIGHTS])
@api_view([HTTPMethod.GET])
@permission_classes([IsAuthenticated, IsManagementUser])
def get_marketZGroupDataInvestorDrillDown(request: Request) -> Response:
    """fetch market Z-group data for investor drilldown"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(MarketZGroupDataInvestorDrillDownORM)
        ).scalars()

        results = [MarketZGroupDataInvestorDrillDown.model_validate(row).model_dump() for row in qs]

    return Response(results)

    

@extend_schema(tags=[OpenApiTags.TRADE_INSIGHTS])
@api_view([HTTPMethod.GET])
@permission_classes([AllowAny])
def get_marketZGroupDataInvestorDrillDowncsv(request: Request) -> Response:
    """fetch market Z-group data for investor drilldown as CSV"""
    request.accepted_renderer = CustomRenderer()

    with Session(engine) as session:
        qs = session.execute(
            select(MarketZGroupDataInvestorDrillDownORM)
        ).scalars()

        results = [MarketZGroupDataInvestorDrillDown.model_validate(row).model_dump() for row in qs]

        header_mapping = {
            "symbol": "Symbol",
            "investor_code": "Investor Code",
            "investor_name": "Investor Name",
            "account_type": "Account Type",
            "current_balance": "Current Balance",
            "ledger_balance": "Ledger Balance",
            "z_buy_qty": "Z Buy Quantity",
            "z_buy_amount": "Z Buy Amount",
            "cash_deposit": "Cash Deposit",
            "non_cash_deposit": "Non-Cash Deposit",
            "used_excess_lbsl_fund": "Used Excess LBSL Fund",
            "fund_using_level": "Fund Using Level",
            "rm_branch": "RM Branch",
            "rm_name": "RM Name",
        }
        remapped_results = [
            {header: row.get(field) for field, header in header_mapping.items()}
            for row in results
        ]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"market_zgroup_investor_drilldown-{timestamp}"
        return generate_csv(remapped_results, list(header_mapping.values()), filename)