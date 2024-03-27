from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request

from authusers.models import User


class ExtendedIsAdminUser(IsAdminUser):
    """Extended version of built-in permission `IsAdminUser` of django rest framework."""

    def has_permission(self, request: Request, _):
        user: User = request.user
        return bool(user and (user.is_staff or user.is_admin()))
