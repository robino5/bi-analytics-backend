from django.urls import path

from . import views

urlpatterns = [
    path("branches/", views.get_branches),
    path("traders/", views.get_all_traders),
    path(
        "traders/<int:id>/",
        views.get_traders_for_branchcode,
    ),
    path(
        "managers/",
        views.get_cluster_managers,
    ),
]
