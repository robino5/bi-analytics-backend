from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChangePasswordAPIView, ProfileViewSet, RoleListAPIView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = [
    path(
        "<str:username>/change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path("roles/", RoleListAPIView.as_view(), name="roles"),
    path("", include(router.urls)),
]
