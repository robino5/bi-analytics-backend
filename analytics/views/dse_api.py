from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from core.metadata.openapi.configs import OpenApiTags
from rest_framework.request import Request
from analytics.views.utils import fetch_from_lankabd_api

__all__ = ["live_dse_trade", "live_tickers"]


@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def live_dse_trade(request: Request):
    data = fetch_from_lankabd_api("/api/datafeed/IndexLiveData/LiveDSETradeStatistics")
    if data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE trade statistics."},
            status=500
        )
    return JsonResponse(data, safe=False)


@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def live_tickers(request: Request):
    data = fetch_from_lankabd_api("/api/datafeed/LiveStockFeed?count=15")
    if data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE ticker data."},
            status=500
        )
    return JsonResponse(data, safe=False)
