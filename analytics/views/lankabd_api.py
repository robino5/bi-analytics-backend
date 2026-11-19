"""
lankabd_api.py

Single entry point for every LankaBD API call:

    from .lankabd_api import fetch_from_lankabd_api

    data = fetch_from_lankabd_api("/api/APIMarket/GetDataGrid")
    data = fetch_from_lankabd_api("/api/Some/Endpoint", params={"a": 1})
    data = fetch_from_lankabd_api("/api/Some/Post", method="POST", json_body={"x": 1})

Returns parsed JSON, or None on any failure (errors are logged).

No Django settings are needed; configuration lives in the constants below.
"""
import hashlib
import hmac
import logging
import time
import uuid
from urllib.parse import urlsplit

import requests

logger = logging.getLogger(__name__)

LANKABD_BASE_URL = "https://lankabd.com"
LANKABD_CLIENT_ID = "idash"
LANKABD_CLIENT_SECRET = "99e80d2e274c7dc3827c2a12548dc3106cd4b242090509c4800d77a067683546"
LANKABD_VERIFY_SSL = True

ANTIFORGERY_PATH = "/lbs/security/antiforgery"


class LankaBDError(Exception):
    pass


class _LankaBDClient:
    def __init__(self):
        self.base_url = LANKABD_BASE_URL.rstrip("/")
        self.client_id = LANKABD_CLIENT_ID
        self.client_secret = LANKABD_CLIENT_SECRET
        self.verify = LANKABD_VERIFY_SSL
        # Session keeps the antiforgery cookie alongside the token header.
        self.session = requests.Session()
        self.session.verify = self.verify
        self.antiforgery_token = None

    def _fetch_antiforgery_token(self):
        resp = self.session.get(f"{self.base_url}{ANTIFORGERY_PATH}", timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success") or not isinstance(data.get("requestToken"), str):
            raise LankaBDError(f"Unexpected antiforgery response: {data}")
        self.antiforgery_token = data["requestToken"]

    def _auth_headers(self, method, path_and_query, body):
        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4()) + str(uuid.uuid4())
        body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest().upper()
        canonical = "\n".join([method, path_and_query, timestamp, nonce, body_hash])
        signature = hmac.new(
            self.client_secret.encode("utf-8"),
            canonical.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest().upper()
        return {
            "X-LB-ClientId": self.client_id,
            "X-LB-Timestamp": timestamp,
            "X-LB-Nonce": nonce,
            "X-LB-Signature": signature,
            "RequestVerificationToken": self.antiforgery_token,
        }

    def call(self, path, method="GET", params=None, json_body=None):
        if not self.client_id or not self.client_secret:
            raise LankaBDError("Missing LANKABD_CLIENT_ID or LANKABD_CLIENT_SECRET")

        method = method.upper()
        self._fetch_antiforgery_token()

        # Prepare first so the signed path+query is exactly what is sent.
        req = requests.Request(
            method, f"{self.base_url}{path}", params=params, json=json_body
        )
        prepared = self.session.prepare_request(req)
        parts = urlsplit(prepared.url)
        path_and_query = parts.path + (f"?{parts.query}" if parts.query else "")

        body = prepared.body or ""
        if isinstance(body, bytes):
            body = body.decode("utf-8")

        prepared.headers.update(self._auth_headers(method, path_and_query, body))
        resp = self.session.send(prepared, timeout=30, verify=self.verify)
        resp.raise_for_status()
        return resp.json()


def fetch_from_lankabd_api(path, method="GET", params=None, json_body=None):
    """Call any LankaBD endpoint. Returns parsed JSON or None on failure."""
    try:
        return _LankaBDClient().call(
            path, method=method, params=params, json_body=json_body
        )
    except (requests.RequestException, LankaBDError, ValueError):
        logger.exception("LankaBD API call failed: %s %s", method, path)
        return None