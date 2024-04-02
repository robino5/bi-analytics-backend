from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = [path("", include(router.urls))]
