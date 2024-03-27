__all__ = ["OpenApiTags", "METADATA_CONFIGS"]


class OpenApiTags:
    Authorization = "authorizations"
    Users = "user-management"
    Token = "token-management"
    LOV = "list-of-values"
    DTP = "daily-trade-performance"
    PM = "portfolio-management"
    MLU = "margin-loan-usage"
    BP = "branch-performance"

    RMWISE_DTP = "rmwise-daily-trade-performance"
    RMWISE_PERFORMANCE = "rmwise-performance"
    RMWISE_PORTFOLIO = "rmwise-portfolio"
    ACTIVE_TRADING_CODE = "active-trading-codes"


openapi_description = r"""
## 🟢 BI Analytics

BI Analytics RestAPI service

**Note:** This API is intended for authorized organizations and internal use only. Unauthorized access is strictly prohibited.
"""

METADATA_CONFIGS = {
    "OAS_VERSION": "3.1.0",
    "TITLE": r"BI Analytics RestAPI",
    "DESCRIPTION": openapi_description,
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SERVE_AUTHENTICATION": None,
    "SWAGGER_UI_SETTINGS": {
        "swagger": "2.0",
        "deepLinking": True,
        "filter": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
    "SERVERS": [
        {"url": "http://127.0.0.1:8000", "description": "LOCAL DEV"},
    ],
    "COMPONENT_SPLIT_REQUEST": True,
}
