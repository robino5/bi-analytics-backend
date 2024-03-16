from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.settings import api_settings

from authusers.views import MyTokenObtainPairView

v1 = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{v1}/auth/", include("authusers.urls")),
    # Open API & Swagger UI
    path(
        "api/openapi",
        SpectacularAPIView.as_view(
            renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
        ),
        name="openapi",
    ),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="openapi"),
        name="swagger-ui",
    ),
    path("api/redoc", SpectacularRedocView.as_view(url_name="openapi"), name="redoc"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="openapi"),
        name="swagger-ui",
    ),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Analytics URL
    path(f"{v1}/dashboards/", include("analytics.urls")),
]
