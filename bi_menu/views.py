from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.renderer import CustomRenderer

from .models import Menu
from .serializers import MenuSerializer

CACHING_TIME = 60 * 60 * 2  # 2 Hour


class MenuViewSet(ViewSet):
    serializer_class = MenuSerializer
    renderer_classes = [CustomRenderer]
    authentication_classes = [JWTAuthentication]
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def _get_root_menus(self):
        return (
            Menu.objects.filter(parent_menu__isnull=True, path__isnull=True)
            .prefetch_related("submenus")
            .order_by("order")
        )

    def get_queryset(self):
        return self._get_root_menus()

    @method_decorator(cache_page(CACHING_TIME))
    @method_decorator(vary_on_headers(settings.HEADER_AUTH_KEY))
    def list(self, request: Request, *args, **kwargs):
        ret = self.serializer_class(self.get_queryset(), many=True)
        return Response(ret.data)

    class Meta:
        model = Menu
