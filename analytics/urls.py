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
    path("basic-summaries/", views.get_basic_summaries),
]
