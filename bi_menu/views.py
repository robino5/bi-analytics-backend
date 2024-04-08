from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.renderer import CustomRenderer

from .models import Menu
from .serializers import MenuSerializer


class MenuViewSet(ViewSet):
    serializer_class = MenuSerializer
    renderer_classes = [CustomRenderer]
    authentication_classes = [JWTAuthentication]
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.order_by("-created_at")

    def list(self, request: Request, *args, **kwargs):
        ret = self.serializer_class(self.get_queryset(), many=True)
        return Response(ret.data)

    class Meta:
        model = Menu
