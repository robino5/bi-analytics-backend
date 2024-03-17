from typing import Any, Dict


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
