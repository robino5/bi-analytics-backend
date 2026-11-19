import csv
import logging
import threading
import time
from typing import Any, Dict, List, Type

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from authusers.models import User
from db import BaseOrm, engine

from ..orm import ClusterManagerOrm

logger = logging.getLogger(__name__)

BASE_URL = "https://lankabd.com"
TIMEOUT = 10
TOKEN_TTL_SECONDS = 10 * 60          # re-scrape token every 10 min
RETRY_STATUS_CODES = {400, 401, 403}  # antiforgery / auth failures
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
)

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

class LankaBDClient:
    """Reusable client: keeps cookies + antiforgery token and refreshes them when needed."""

    def __init__(self, base_url: str = BASE_URL, timeout: int = TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": self.base_url + "/",
            "X-Requested-With": "XMLHttpRequest",
        })
        self._token = ""
        self._token_at = 0.0
        self._lock = threading.Lock()

    # ---------- token handling ----------
    def _refresh_token(self) -> None:
        """Load the homepage: sets fresh cookies on the session and extracts the token."""
        self._session.cookies.clear()
        res = self._session.get(self.base_url, timeout=self.timeout)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        node = soup.find("input", {"name": "__RequestVerificationToken"})
        if not node or not node.get("value"):
            raise RuntimeError("Antiforgery token not found on homepage")

        self._token = node["value"]
        self._token_at = time.time()

    def _ensure_token(self, force: bool = False) -> None:
        with self._lock:
            expired = (time.time() - self._token_at) > TOKEN_TTL_SECONDS
            if force or not self._token or expired:
                self._refresh_token()

    # ---------- generic request ----------
    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict | None = None,
        json: Any = None,
        data: Any = None,
        headers: dict | None = None,
    ) -> Any:
        """Call any endpoint. Retries once with a fresh token if the server rejects it."""
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}/{endpoint.lstrip('/')}"

        for attempt in (1, 2):
            self._ensure_token(force=(attempt == 2))
            req_headers = {"RequestVerificationToken": self._token, **(headers or {})}

            response = self._session.request(
                method.upper(), url,
                params=params, json=json, data=data,
                headers=req_headers, timeout=self.timeout,
            )

            if response.status_code in RETRY_STATUS_CODES and attempt == 1:
                logger.warning("LankaBD %s %s -> %s, refreshing token", method, endpoint, response.status_code)
                continue

            response.raise_for_status()
            return response.json() if response.content else None


# One shared instance per process
_client = LankaBDClient()


def call_lankabd_api(
    endpoint: str,
    method: str = "GET",
    *,
    params: dict | None = None,
    json: Any = None,
    data: Any = None,
) -> Any | None:
    """Returns parsed JSON, or None on failure."""
    try:
        return _client.request(method, endpoint, params=params, json=json, data=data)
    except Exception:
        logger.exception("LankaBD call failed: %s %s", method, endpoint)
        return None


def lankabd_response(
    endpoint: str,
    method: str = "GET",
    *,
    params: dict | None = None,
    json: Any = None,
    error_message: str = "Failed to fetch live data.",
) -> JsonResponse:
    """Call the API and return a ready-to-use Django JsonResponse."""
    data = call_lankabd_api(endpoint, method, params=params, json=json)
    if data is None:
        return JsonResponse({"error": error_message}, status=502)
    return JsonResponse(data, safe=False)


# Backward compatible with your old code
def fetch_from_lankabd_api(endpoint: str) -> dict | None:
    return call_lankabd_api(endpoint)

    
def fetchAamarStockWeb(endpoint: str):
    response = requests.get(endpoint)
    response.raise_for_status()
    return response.json()