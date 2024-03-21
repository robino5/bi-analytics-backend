from typing import Any, Dict, Type

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from authusers.models import User
from db import BaseOrm, engine

from ..orm import ClusterManagerOrm


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


def inject_branchwise_filter(
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
