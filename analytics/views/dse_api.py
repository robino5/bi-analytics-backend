import requests
import re
from bs4 import BeautifulSoup
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from http import HTTPMethod
from core.metadata.openapi.configs import OpenApiTags
from rest_framework.request import Request

__all__ = [
    "live_dse_trade",
]


def get_token_and_cookies():
    """
    Fetch Lankabd home page to extract fresh cookies and verification token.
    """
    session = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }

    home_url = "https://lankabd.com"
    res = session.get(home_url, headers=headers, timeout=10)
    res.raise_for_status()

    # Extract RequestVerificationToken from HTML <input>
    soup = BeautifulSoup(res.text, 'html.parser')
    token_input = soup.find("input", {"name": "__RequestVerificationToken"})
    token = token_input["value"] if token_input else ""

    return session.cookies.get_dict(), token


def fetch_live_dse_trade_stats_requests():
    url = "https://lankabd.com/api/datafeed/IndexLiveData/LiveDSETradeStatistics"

    try:
        # Get fresh cookies and token
        cookies_dict, token = get_token_and_cookies()

        # Reformat cookies to header string
        cookie_header = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': cookie_header,
            'Host': 'lankabd.com',
            'Referer': 'https://lankabd.com/',
            'RequestVerificationToken': token,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="138", "Google Chrome";v="138", "Not)A;Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        # Make API request with dynamic cookies/token
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("❌ Error fetching DSE data:", e)
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
