from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChangePasswordAPIView, ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = [
    path(
        "<str:username>/change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path("", include(router.urls)),
]
