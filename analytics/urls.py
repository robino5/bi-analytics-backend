from django.urls import path

from . import views

urlpatterns = [
    path("lov/branches/", views.get_branches),
    path("lov/traders/", views.get_all_traders),
    path(
        "lov/traders/<int:id>/",
        views.get_traders_for_branchid,
    ),
    path(
        "lov/managers/",
        views.get_cluster_managers,
    ),
    # Daily Trade Performance Routes
    path("basic-summaries/", views.get_basic_summaries),
    path("basic-summaries/<int:id>", views.get_basic_summaries_by_branchid),
    path("daily-trade-performance/", views.get_turnover_performance_statistics),
    path(
        "daily-trade-performance/<int:id>",
        views.get_turnover_performance_statistics_by_branchid,
    ),
    path("margin-loan-usage/", views.get_margin_loan_statistics),
    path("margin-loan-usage/<int:id>", views.get_margin_loan_statistics_by_branchid),
    path("sector-exposure-cashcode/", views.get_cashcode_sector_exposure),
    path(
        "sector-exposure-cashcode/<int:id>",
        views.get_cashcode_sector_exposure_by_branchid,
    ),
    path("sector-exposure-margincode/", views.get_margincode_sector_exposure),
    path(
        "sector-exposure-margincode/<int:id>",
        views.get_margincode_sector_exposure_by_branchid,
    ),
    # Portfolio Management Routes
    path("daily-net-fundflow/", views.get_daily_net_fundflow),
    path("daily-net-fundflow/<int:id>", views.get_daily_net_fundflow_by_branchid),
    path("trade-vs-clients/", views.get_trade_vs_client_statistics),
    path("trade-vs-clients/<int:id>", views.get_trade_vs_client_statistics_by_branchid),
    path("turnover-performance/", views.get_turnover_performance),
    path("turnover-performance/<int:id>", views.get_turnover_performance_by_branchid),
    path("accounts-fundflow/", views.get_accounts_fundflow),
    path("accounts-fundflow/<int:id>", views.get_accounts_fundflow_by_branchid),
    path("portfolio-status/", views.get_portfolio_status),
    path("portfolio-status/<int:id>", views.get_portfolio_status_by_branchid),
    # Margin Loan Usage Routes
    path("margin-loan-allocations/", views.get_margin_loan_allocations),
    path(
        "margin-loan-allocations/<int:id>",
        views.get_margin_loan_allocations_by_branchid,
    ),
    path("exposure-list/", views.get_exposures_list),
    path("exposure-list/<int:id>", views.get_exposures_list_by_branchid),
    path("rmwise-net-trades/", views.get_rmwise_net_trades),
    path("zonewise-investors/", views.get_zone_marked_clients),
]
