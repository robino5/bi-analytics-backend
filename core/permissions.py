from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.request import Request

from authusers.models import User


class ExtendedIsAdminUser(IsAdminUser):
    """Extended version of built-in permission `IsAdminUser` of django rest framework."""

    def has_permission(self, request: Request, _):
        user: User = request.user
        return bool(user and (user.is_staff or user.is_admin()))


class IsManagementUser(BasePermission):
    def has_permission(self, request, _):
        return bool(
            request.user and request.user.is_management or request.user.is_admin()
        )

    def has_object_permission(self, request: Request, view, obj):
        return True
