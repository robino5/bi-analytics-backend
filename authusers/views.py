import json
from http import HTTPMethod
from logging import getLogger

from django.contrib.auth.hashers import make_password
from django_filters import rest_framework as filters
from djangorestframework_camel_case.parser import (
    CamelCaseJSONParser,
    CamelCaseMultiPartParser,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from core.helper import EmptySerializer, enveloper
from core.metadata.openapi import OpenApiTags
from core.permissions import ExtendedIsAdminUser
from core.renderer import CustomRenderer

from .filter import UserFilter
from .models import Trader, User, UserProfile
from .serializers import (
    BulkUserCreateSerializer,
    MyTokenObtainPairSerializer,
    ProfileSerializer,
    TraderSerializer,
    UserSerializer,
)

logging = getLogger("authusers.views")


class UserNotFoundException(exceptions.APIException):
    default_detail = "User Not Found !"
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "not_found"


class InvalidPayloadException(exceptions.APIException):
    default_code = "validation_error"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Validation Error"


class PermissionDeniedException(exceptions.APIException):
    default_code = "permission_error"
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You're not authorized to perform this action."


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
    pagination_class = None
    permission_classes = [IsAuthenticated, ExtendedIsAdminUser]
    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.all().order_by("-created_at")

    def get_permissions(self):
        if self.action in (["actions_by_username"]):
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

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
    def create(self, request: Request, *args, **kwargs):
        request.data["created_by"] = request.user.pk
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def update(self, request, *args, **kwargs):
        request.data["updated_by"] = request.user.pk
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def partial_update(self, request, *args, **kwargs):
        request.data["updated_by"] = request.user.pk
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        responses={204: enveloper(EmptySerializer, many=False)},
        tags=[OpenApiTags.Users],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(TraderSerializer, many=False),
        tags=[OpenApiTags.Users],
    )
    @action(methods=[HTTPMethod.GET], detail=False, url_path="noaccounts")
    def find_users_without_accounts(self, request: Request):
        query = Trader.objects.exclude(
            trader_id__in=User.objects.values("username")
        ).all()

        return Response(TraderSerializer(query, many=True).data)

    @extend_schema(
        request=BulkUserCreateSerializer(),
        tags=[OpenApiTags.Users],
    )
    @action(methods=[HTTPMethod.POST], detail=False, url_path="bulkusers")
    def create_bulk_users(self, request: Request):
        serialized = BulkUserCreateSerializer(data=request.data)

        if not serialized.is_valid():
            raise InvalidPayloadException(serialized.errors)
        hashed_passwd = make_password(serialized.validated_data["password"])
        role = serialized.validated_data["role"]
        objs = (
            {"username": username, "password": hashed_passwd, "role": role}
            for username in serialized.validated_data["users"]
        )
        # TODO: this is wrong ! as this is doing each transaction roundtrip to database. But need this for now to
        # properly work with Django Signals
        for user in objs:
            user = User(**user)
            user.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    @action(
        methods=[HTTPMethod.GET, HTTPMethod.PATCH, HTTPMethod.DELETE],
        detail=True,
        url_path="by-username",
    )
    def actions_by_username(self, request: Request, pk: str):
        current_user: User = request.user

        if not current_user.is_admin() and current_user.username != pk:
            logging.warning(
                f"'!!!' {request.user!r} is violating ACL. Trying to take action for User<{pk!r}> profile. '!!!'"
            )
            raise PermissionDeniedException()

        try:
            instance = User.objects.get(username=pk)
        except User.DoesNotExist as exc:
            logging.warning(
                f"'!!!' {request.user!r} tried to edit User<{pk!r}> profile which doesn't exists in system. '!!!'"
            )
            raise UserNotFoundException from exc

        if request.method == HTTPMethod.DELETE:
            if not current_user.is_admin():
                logging.warning(
                    f"'!!!' {request.user!r} is violating ACL. Trying to delete for User<{pk!r}> profile. '!!!'"
                )
                raise PermissionDeniedException()

            instance.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        if request.method == HTTPMethod.PATCH:
            if not current_user.is_admin():
                request.data.pop("role", None)
                request.data.pop("is_active", None)

            profile = request.data.pop("profile", None)
            request.data.pop("username", None)  # remove username edit
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
                _serialized_user.validated_data["updated_by"] = request.user
                _serialized_user.save()
            except exceptions.ValidationError as exc:
                logging.exception(exc)
                raise InvalidPayloadException from exc

            logging.info(f"profile 'partial_update' successful for {instance!r}")
            return Response(_serialized_user.data)

        logging.info(f"profile 'get' successful for {instance!r}")
        return Response(self.serializer_class(instance=instance).data)


class ProfileViewSet(ViewSet):
    serializer_class = ProfileSerializer
    parser_classes = [CamelCaseMultiPartParser, CamelCaseJSONParser]
    renderer_classes = [CustomRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.all().order_by("-pk")

    @extend_schema(
        parameters=CUSTOM_ID_USER_PARAMETERS,
        responses=enveloper(UserSerializer, many=False),
    )
    def partial_update(self, request: Request, pk: str):
        current_user: User = request.user

        if not current_user.is_admin() and current_user.username != pk:
            logging.warning(
                f"'!!!' {request.user!r} is violating ACL. Trying to 'partial_update' User<{pk!r}> profile. '!!!'"
            )
            raise PermissionDeniedException()
        try:
            instance = User.objects.get(username=pk)
        except User.DoesNotExist as exc:
            logging.warning(
                f"'!!!' {request.user!r} tried to 'partial_update' User<{pk!r}> profile, which doesn't exists in system. '!!!'"
            )
            raise UserNotFoundException() from exc

        profile = instance.profile

        _serialized_profile = self.serializer_class(
            instance=profile, data=request.data, partial=True
        )

        if not _serialized_profile.is_valid():
            logging.error(
                msg=f"'partial_update' failed for {instance!r} due to 'validation_error'. Errors:{json.dumps(_serialized_profile.errors)}",
            )
            return Response(_serialized_profile.errors)

        instance.updated_by = request.user
        _serialized_profile.save()
        logging.info(f"'partial_update' finished for {instance!r}")
        return Response(UserSerializer(instance=instance).data)


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
