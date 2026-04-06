from http import HTTPMethod
from datetime import datetime
import os
import pyodbc

from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from core.metadata.openapi.configs import OpenApiTags
from rest_framework.request import Request

__all__ = ["execute_branch_performance_sp","execute_region_wise_management_sp"]


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "start_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="Start date (YYYY-MM-DD)"),
        OpenApiParameter(
            "end_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="End date (YYYY-MM-DD)"),
    ],
)
@api_view([HTTPMethod.POST])
def execute_branch_performance_sp(request: Request):
    """Execute stored procedure BIAnalytics_Region_Wise_MarketInsight_BranchPerformance_Date_Duration

    Expects JSON body or query params: `start_date` and `end_date` in YYYY-MM-DD format.
    Connection uses SQL Server at 192.168.100.20 with credentials provided by the user.
    """

    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    if not start_date or not end_date:
        return JsonResponse({"error": "start_date and end_date are required"}, status=400)

    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return JsonResponse({"error": "Date format must be YYYY-MM-DD"}, status=400)

    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=192.168.100.20;"
            "DATABASE=MintDB;"
            "UID=sa;"
            "PWD=leads@123;",
            autocommit=True
        )

        cursor = conn.cursor()

        cursor.execute(
            "EXEC BIAnalytics_Region_Wise_MarketInsight_BranchPerformance_Date_Duration ?, ?",
            start_date,
            end_date,
        )

        conn.commit()
        # move to first result set that has data
        while cursor.description is None:
            if not cursor.nextset():
                return JsonResponse({"data": []})

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


@extend_schema(
    tags=[OpenApiTags.RBP],
    parameters=[
        OpenApiParameter(
            "start_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="Start date (YYYY-MM-DD)"),
        OpenApiParameter(
            "end_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="End date (YYYY-MM-DD)"),
    ],
)
@api_view([HTTPMethod.POST])
def execute_region_wise_management_sp(request: Request):
    """Execute stored procedure BIAnalytics_Region_Wise_MarketInsight_RegionWiseManagement_Date_Duration

    Expects JSON body or query params: `start_date` and `end_date` in YYYY-MM-DD format.
    Connection uses SQL Server at 192.168.100.20 with credentials provided by the user.
    """

    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    if not start_date or not end_date:
        return JsonResponse({"error": "start_date and end_date are required"}, status=400)

    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return JsonResponse({"error": "Date format must be YYYY-MM-DD"}, status=400)

    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=192.168.100.20;"
            "DATABASE=MintDB;"
            "UID=sa;"
            "PWD=leads@123;",
            autocommit=True
        )

        cursor = conn.cursor()

        cursor.execute(
            "EXEC BIAnalytics_Region_Wise_Management_data_AsonDate ?, ?",
            start_date,
            end_date,
        )

        conn.commit()
        # move to first result set that has data
        while cursor.description is None:
            if not cursor.nextset():
                return JsonResponse({"data": []})

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
