from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MenuViewSet

router = DefaultRouter()
router.register("", MenuViewSet, basename="menus")

urlpatterns = [path("", include(router.urls))]
