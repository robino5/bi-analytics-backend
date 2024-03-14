from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from core.helper import EmptySerializer, enveloper
from core.renderer import CustomRenderer

from .filter import UserFilter
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    renderer_classes = (CustomRenderer,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.all().order_by("-created_at")

    @extend_schema(responses=enveloper(UserSerializer, many=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(responses=enveloper(UserSerializer, many=False))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(responses=enveloper(UserSerializer, many=False))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(responses=enveloper(UserSerializer, many=False))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(responses=enveloper(UserSerializer, many=False))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(responses={204: enveloper(EmptySerializer, many=False)})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
