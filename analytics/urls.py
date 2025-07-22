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
    path("rmwise-net-trades/<int:id>", views.get_rmwise_net_trades_by_branch_id),
    path("zonewise-investors/", views.get_zone_marked_clients),
    # Branch Wise Performance
    path("branchwise-turnover-status/", views.get_bw_turnover_status),
    path("branchwise-margin-status/", views.get_bw_margin_status),
    path("branchwise-fund-status/", views.get_bw_fund_status),
    path("branchwise-exposure-status/", views.get_bw_exposure_status),
    ################# RM Wise Dashboards URL ##########################
    # Daily Trade Performance
    path("rm/basic-summaries/", views.get_basic_summaries_rmwise),
    path(
        "rm/daily-trade-performance/", views.get_turnover_performance_statistics_rmwise
    ),
    path(
        "rm/sector-exposure-cashcode/",
        views.get_cashcode_sector_exposure_rmwise,
    ),
    path("rm/sector-exposure-margincode/", views.get_margincode_sector_exposure_rmwise),
    path("rm/turnover-performance/", views.get_turnover_perfomance_rmwise),
    path("rm/client-details/", views.get_client_detail_rmwise),
     path("rm/daily-trade-data/", views. get_rmwise_daily_trade_date),
    # RM portfolio
    path("rm/fund-collections/", views.get_fund_collection_rmwise),
    path("rm/portfolio-management-status/", views.get_portfolio_management_rmwise),
    path("rm/daily-net-fund-flow/", views.get_daily_net_fund_flow_rmwise),
    path("rm/marked-clients/", views.get_zone_marked_clients_rmwise),
    path("rm/ecrm-details/", views.get_ecrm_details_rmwise),
    # Active Trading Codes Route
    path("active-trading-today/", views.get_active_trading_summary),
    path("active-trading-daywise/", views.get_active_trading_summary_daywise),
    path("active-trading-monthwise/", views.get_active_trading_monthwise_client),
    path("admin-oms-branchwise-turnover/", views.get_admin_oms_branch_wise_turnover_as_on_month),
    path("admin-oms-branchwise-turnover-dt/", views.get_admin_oms_branch_wise_turnover_dt_as_on_month),
    path("admin-oms-branchwise-turnover-csv/", views.download_admin_oms_datewise_turnover_csv),
    path("admin-oms-branchwise-dt-turnover-csv/", views.download_admin_oms_datewise_dt_turnover_csv),
    path("admin-oms-datewise-turnover/", views.get_admin_oms_datewise_turnover),
    path("admin-sector-wise-turnover/", views.get_admin_sector_wise_turnover),
    path("admin-sector-wise-turnover-breakdown/", views.get_admin_sector_wise_turnover_breakdown),
    path("admin-realtime-turnover-top-20/", views.get_admin_realtime_turnover_top_20),
    path("admin-realtime-turnover-exchange-top-20/", views.get_admin_realtime_turnover_exchange_top_20),
    path("admin-realtime-turnover-comparison-sector-wise/", views.get_admin_realtime_turnover_comaparison_sector_wise),
    path("admin-realtime-turnover-comparison-top20-sector-wise/", views.get_admin_realtime_turnover_comaparison_top20_sector_wise),
    path("admin-realtime-turnover-comparison-top20-sector-wise/", views.get_admin_realtime_turnover_comaparison_top20_sector_wise),

    # portal live data
    path("portal-dse-live-trade/", views.live_dse_trade),
    path("portal-live-tickers/", views.live_tickers),
    # Business And Trade Management
    path("admin/board-turnover/", views.get_board_turnovers),
    path("admin/board-turnovers-breakdown/", views.get_board_turnovers_breakdown),
    path("admin/market-share-details/", views.get_market_share_details),
    path("admin/atb-market-share-details/", views.get_atb_markte_share_details),
    path("admin/companywise-saleable-stock/", views.get_company_wise_saleable_stock),
    path("admin/investorwise-saleable-stock/", views.get_investor_wise_saleable_stock),
    path(
        "admin/companywise-saleable-stock-percentage/",
        views.get_company_wise_saleable_stock_percentage,
    ),
    # Admin Customer Management
    path(
        "admin/customer-management/client-segmentations/",
        views.get_client_segmentation_summary,
    ),
    path(
        "admin/customer-management/branchwise-client-ratio/",
        views.get_branchwise_client_numbers_ratio,
    ),
    path(
        "admin/customer-management/branchwise-non-performers/",
        views.get_non_performers_client_ratio,
    ),
    path(
        "admin/customer-management/turnover-segmentation/",
        views.get_admin_client_segmentation_turnover,
    ),
    path(
        "admin/customer-management/tpv-segmentation/",
        views.get_admin_client_segmentation_tpv,
    ),
    path(
        "admin/customer-management/equity-segmentation/",
        views.get_admin_client_segmentation_equity,
    ),
    path(
        "admin/customer-management/ledger-segmentation/",
        views.get_admin_client_segmentation_ledger,
    ),
    path(
        "admin/customer-management/market-share-segmentation/",
        views.get_admin_market_share,
    ),
    path(
        "admin/customer-management/gsec-turnover/",
        views.get_admin_gsec_turnover,
    ),
    path(
        "admin/customer-management/gsec-turnover-comparison/",
        views.get_admin_gsec_turnover_comparison,
    ),
]
