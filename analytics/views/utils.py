from typing import Any, Dict, Type,List
import csv
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from django.http import HttpResponse
from authusers.models import User
from db import BaseOrm, engine
import requests
from bs4 import BeautifulSoup

from ..orm import ClusterManagerOrm

BASE_URL = "https://lankabd.com"
TIMEOUT = 10


def parse_summary(data: Dict[str, Any], key: str) -> dict:
    """utility function to parse the summary data of the daily performance board"""
    _categories = {
        "short_summary": [
            "total_clients",
            "total_active_clients",
            "daily_turnover",
            "net_buy_sell",
        ],
        "cash_code_summary": [
            "cash_balance",
            "cash_stock_balance",
            "cash_daily_turnover",
            "cash_active_clients",
        ],
        "margin_code_summary": [
            "margin_balance",
            "margin_stock_balance",
            "margin_active_clients",
            "margin_daily_turnover",
        ],
    }

    return {key: {category: data[category] for category in _categories[key]}}


def rolewise_branch_data_filter(
    queryset: Select,
    user: User,
    orm_class: Type[BaseOrm],
):
    qs = queryset

    with Session(engine) as session:
        if user.is_cluster_manager():
            branches_qs = select(ClusterManagerOrm.branch_code).where(
                ClusterManagerOrm.manager_name == user.username
            )
            branch_codes = [result[0] for result in session.execute(branches_qs)]
            qs = queryset.where(orm_class.branch_code.in_(branch_codes))
        if user.is_branch_manager():
            qs = queryset.where(orm_class.branch_code == user.profile.branch_id)

    return qs



def generate_csv(data: List[dict], headers: List[str], filename: str) -> HttpResponse:
    """
    Generate and return a CSV response for the provided data.

    :param data: List of dictionaries containing the rows for the CSV.
    :param headers: List of strings representing the column headers for the CSV.
    :param filename: The name of the CSV file to download.
    :return: HttpResponse with the CSV file.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    writer.writerow(headers) 

    for row in data:
        writer.writerow([row.get(header, "") for header in headers])  

    return response


def get_token_and_cookies() -> tuple[dict, str]:
    """
    Fetch Lankabd homepage to extract cookies and verification token.
    """
    session = requests.Session()
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        )
    }

    res = session.get(BASE_URL, headers=headers, timeout=TIMEOUT)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    token_input = soup.find("input", {"name": "__RequestVerificationToken"})
    token = token_input["value"] if token_input else ""
    return session.cookies.get_dict(), token


def build_headers(cookies: dict, token: str) -> dict:
    cookie_header = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    return {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookie_header,
        'Host': 'lankabd.com',
        'Referer': BASE_URL + '/',
        'RequestVerificationToken': token,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="138", "Google Chrome";v="138", "Not)A;Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


def fetch_from_lankabd_api(endpoint: str) -> dict | None:
    """
    Fetch data from a Lankabd API endpoint with fresh cookies and token.
    """
    try:
        cookies, token = get_token_and_cookies()
        headers = build_headers(cookies, token)
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching data from {endpoint}: {e}")
        return None