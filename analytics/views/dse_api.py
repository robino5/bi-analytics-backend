from datetime import datetime, timedelta
import time
from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema,OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from core.metadata.openapi.configs import OpenApiTags
from rest_framework.request import Request
from analytics.views.utils import fetch_from_lankabd_api,fetchAamarStockWeb

__all__ = ["live_dse_trade",
            "live_tickers",
            "live_dse_dsex",
            "live_dse_dsex_summary",
            "dse_dsex_trade_summary_previous_ten_days",
            "fear_greed",
            "stock_pe_ration",
            "dse_traded_company_list",
            "get_poral_pe_rsi_conpanywise",
            "dse_history_company"
            ]


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

@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def live_dse_dsex(request: Request):
    data = fetch_from_lankabd_api("/api/datafeed/IndexLiveData/LiveIndexSummary?symbol=DSEX")
    if data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE ticker data."},
            status=500
        )
    return JsonResponse(data, safe=False)

@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def live_dse_dsex_summary(request: Request):
    data = fetch_from_lankabd_api("/api/datafeed/IndexLiveData/LiveIndexSummaryCDP?symbol=DSEX")
    if data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE ticker data."},
            status=500
        )
    return JsonResponse(data, safe=False)

@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def dse_dsex_trade_summary_previous_ten_days(request: Request):
    data = fetch_from_lankabd_api("/api/APIMarket/GetTradeStatisitcsHistory?count=10")
    if data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE ticker data."},
            status=500
        )
    return JsonResponse(data, safe=False)



@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def fear_greed(request: Request):
    try:
        data = fetchAamarStockWeb("https://www.amarstock.com/Home/GetFearGreedOnly")
        return JsonResponse(data, safe=False)  
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def stock_pe_ration(request: Request):
    try:
        data = fetchAamarStockWeb("https://www.amarstock.com/pe-data-chart")
        return JsonResponse(data, safe=False)  
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def dse_traded_company_list(request: Request):
    data = fetch_from_lankabd_api("/api/datafeed/IndexLiveData/LiveStockWatchData")
    if data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE ticker data."},
            status=500
        )
    return JsonResponse(data, safe=False)


@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA],
                  parameters=[
        OpenApiParameter(
            "company_code",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            required=True,
            description="Company Code Of the DSE",
        )]
               )
@api_view(["GET"])
def get_poral_pe_rsi_conpanywise(request: Request):
    company_code = request.query_params.get("company_code", "")

    # API URLs
    stock_statistics_url = f"/api/company/StockStatisticsV2?cid={company_code}"
    latest_mk_data_url = f"/api/Company/LatestMkDataSymbol?cid={company_code}"

    # Fetch data
    stock_statistics = fetch_from_lankabd_api(stock_statistics_url)
    latest_mk_data = fetch_from_lankabd_api(latest_mk_data_url)

    if stock_statistics is None or latest_mk_data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE ticker data."},
            status=500
        )

    # --- Extract numeric pe_ratio ---
    pe_ratio = None
    if isinstance(stock_statistics, list) and len(stock_statistics) > 0:
        first_item = stock_statistics[0]
        pe_key = next((k for k in first_item.keys() if k.startswith("P/E (Interim)")), None)
        if pe_key:
            try:
                pe_ratio = float(first_item.get(pe_key))
            except (ValueError, TypeError):
                pe_ratio = None

    # --- Extract numeric RSI ---
    rsi = None
    if isinstance(latest_mk_data, list) and len(latest_mk_data) >= 2:
        try:
            rsi = float(latest_mk_data[-2])
        except (ValueError, TypeError):
            rsi = None

    response_data = {
        "pe_ratio": pe_ratio,
        "rsi": rsi,
    }

    return JsonResponse(response_data, safe=False)




@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA],
        parameters=[
        OpenApiParameter(
            "symbol",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="Company Symbol Of the DSE",
        )]
               )
@extend_schema(tags=[OpenApiTags.PORTAL_LIVE_DATA])
@api_view(["GET"])
def dse_history_company(request: Request):
    # ✅ Get symbol from query params
    symbol = request.query_params.get("symbol")
    if not symbol:
        return JsonResponse(
            {"error": "Symbol parameter is required."},
            status=400
        )

    # ✅ Calculate date range: from = 1 month ago, to = today
    today = datetime.now()
    one_month_ago = today - timedelta(days=30)

    # ✅ Convert to UNIX timestamp (seconds)
    to_timestamp = int(time.mktime(today.timetuple()))
    from_timestamp = int(time.mktime(one_month_ago.timetuple()))

    # ✅ Build URL dynamically
    url = f"/tvc/DataFeed/history?symbol={symbol}&resolution=D&from={from_timestamp}&to={to_timestamp}&dataType=false&isAdjusted=false&is"

    # ✅ Fetch data
    data = fetch_from_lankabd_api(url)
    if data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE ticker data."},
            status=500
        )

    return JsonResponse(data, safe=False)