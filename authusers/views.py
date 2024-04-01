from http import HTTPMethod

from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from core.helper import EmptySerializer, enveloper
from core.metadata.openapi import OpenApiTags
from core.permissions import ExtendedIsAdminUser
from core.renderer import CustomRenderer

from .filter import UserFilter
from .models import User
from .serializers import (
    MyTokenObtainPairSerializer,
    ProfileSerializer,
    UserSerializer,
)


class UserNotFoundException(exceptions.APIException):
    default_detail = "User Not Found !"
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "not_found"


class InvalidPayloadException(exceptions.APIException):
    default_code = "validation_error"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Validation Error"


CUSTOM_ID_USER_PARAMETERS = [
    OpenApiParameter(
        name="id",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.PATH,
        required=True,
    )
]


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer]
    filter_backends = [filters.DjangoFilterBackend]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ExtendedIsAdminUser]
    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.all().order_by("-created_at")

    @extend_schema(
        responses=enveloper(UserSerializer, many=True), tags=[OpenApiTags.Users]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        responses={204: enveloper(EmptySerializer, many=False)},
        tags=[OpenApiTags.Users],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
            )
        ],
        responses=enveloper(EmptySerializer, many=False),
        tags=[OpenApiTags.Users],
    )
    @action(
        methods=[HTTPMethod.GET, HTTPMethod.PATCH, HTTPMethod.DELETE],
        detail=True,
        url_path="by-username",
    )
    def actions_by_username(self, request: Request, pk: str):
        try:
            instance = User.objects.get(username=pk)
        except User.DoesNotExist as exc:
            raise UserNotFoundException from exc

        if request.method == HTTPMethod.DELETE:
            instance.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        if request.method == HTTPMethod.PATCH:
            profile = request.data.pop("profile", None)
            request.data.pop("username", None)  # remove username edit
            request.data.pop("password", None)  # remove password edit
            try:
                if profile:
                    _serialized_profile = ProfileSerializer(
                        instance=instance.profile, data=profile, partial=True
                    )
                    _serialized_profile.is_valid(raise_exception=True)
                    _serialized_profile.save()
                _serialized_user = self.serializer_class(
                    instance=instance, data=request.data, partial=True
                )

                _serialized_user.is_valid(raise_exception=True)
                _serialized_user.save()
            except exceptions.ValidationError as exc:
                raise InvalidPayloadException from exc

            return Response(_serialized_user.data)

        return Response(self.serializer_class(instance=instance).data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    renderer_classes = (CustomRenderer,)

    @extend_schema(
        tags=[OpenApiTags.Token],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            current_user = User.objects.get(username=request.data.get("username"))
            user = UserSerializer(instance=current_user)
            payload = user.data
            payload["designation"] = current_user.profile.designation
            payload["access_token"] = serializer.validated_data.get("access")
            payload["refresh_token"] = serializer.validated_data.get("refresh")
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e
        except User.DoesNotExist:
            raise

        return Response(payload, status=status.HTTP_200_OK)
