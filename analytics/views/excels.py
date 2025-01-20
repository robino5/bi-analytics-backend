from http import HTTPMethod
from sqlalchemy import select
from sqlalchemy.orm import Session
from analytics.views.utils import generate_csv
from db import engine
from datetime import datetime

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes

from core.metadata.openapi.configs import OpenApiTags

from rest_framework.permissions import IsAuthenticated
from core.permissions import IsManagementUser

from ..models import (
    AdminOMSBranchWiseTurnoverAsOnMonth
)
from ..orm import (
    AdminOMSBranchWiseTurnoverAsOnMonthORM
)

__all__ = [
    "download_admin_oms_datewise_turnover_csv"
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
