from django.contrib.auth.models import AbstractUser
from django.db import models

from core.mixins import AuditLogMixin

from .managers import BaseUserManager


class RoleChoices(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    BRANCH_MANAGER = "BRANCH_MANAGER", "Branch Manager"
    REGIONAL_MANAGER = "REGIONAL_MANAGER", "Regional Manager"
    CLUSTER_MANAGER = "CLUSTER_MANAGER", "Cluster Manager"


class User(AbstractUser, AuditLogMixin):
    role = models.CharField(
        max_length=55, choices=RoleChoices.choices, default=RoleChoices.REGIONAL_MANAGER
    )

    objects = BaseUserManager()

    def __str__(self) -> str:
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(blank=True, null=True, verbose_name="Profile Pic")
    branch_id = models.IntegerField(null=True, blank=True, verbose_name="Branch Id")
    branch_name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Branch Name"
    )

    def __str__(self) -> str:
        return f"{self.user.username.title()} Profile"
