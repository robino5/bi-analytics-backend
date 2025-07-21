
import requests
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from http import HTTPMethod
from core.metadata.openapi.configs import OpenApiTags
from rest_framework.request import Request
import traceback

__all__ = [
    "live_dse_trade",
]


def fetch_live_dse_trade_stats_requests():
    url = "https://lankabd.com/api/datafeed/IndexLiveData/LiveDSETradeStatistics"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'css=%2Fcss%2Fdefault.css; .AspNetCore.Antiforgery.Vb0oIggZdf4=CfDJ8EpbMnWQA0xBh2wNlKw67qyOITuPKT9GBtnu0UMpX821_VetpqUoO1RAbGH-XPvLMTtlcCmtLbBWxGxVizSIaTjvVJhVBjS53O4cI6s62k8Fa3iLz0e6ns5aQ7mN9QnPEIPeFD_JloRfAfetORGheO8; _gid=GA1.2.1569163892.1752985444; _ga=GA1.1.283324304.1730778201; TS018d6087=018bd698e10e9726923d0c552538779e9d206904c254bb5b32a852479dc6025435ae99542ff107682606276241a3decf54bfc6e5bd64070dbdd4157168e32d2d6f274c07d7d6f1bd4d45756c9890ea053e2719c821; ExchangeID=1; _ga_JW9REK4KKZ=GS2.1.s1752985150$o456$g1$t1752990234$j60$l0$h0; TS086c0efa027=08c9663e84ab20002df2402cec986c4b651eece2527a990c68319ec8e827ee8f4a1a1a662beb124908b787701e11300086489fb10d3c5bd66b0dc35e986e4b8dc30b008704b6fa30c96e9e60a81f0bb346a23adf961b45c49400bbaa8c09d433',
        'Host': 'lankabd.com',
        'Referer': 'https://lankabd.com/',
        'RequestVerificationToken': 'CfDJ8EpbMnWQA0xBh2wNlKw67qxwZDjhsN1ibLka7_Nhr6ZFfEZMNF8AOFdo8t0ciXA6-eS1_uWd4ziQ1C_DLerBdpq4odkgAFiSeSrjCOWcRbAYVlqTSwLAkeLGom2Rf44-5LVOxUGd2BoaO_jZfRy2tpA',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'sec-ch-ua': '''Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138''',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("❌ Error occurred:")
        traceback.print_exc()
        return None


@extend_schema(tags=[OpenApiTags.ACTIVE_TRADING_CODE])
@api_view([HTTPMethod.GET])
def live_dse_trade(request: Request):
    data = fetch_live_dse_trade_stats_requests()
    if data is None:
        return JsonResponse(
            {"error": "Failed to fetch live DSE trade statistics."},
            status=500
        )
    return JsonResponse(data, safe=False)

