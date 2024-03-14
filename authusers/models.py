from django.contrib.auth.models import AbstractUser
from django.db import models

from core.mixins import AuditLogMixin


class RoleChoices(models.TextChoices):
    ADMIN = "admin", "Admin"
    BRANCH_MANAGER = "branch_manager", "Branch Manager"
    REGIONAL_MANAGER = "regional_manager", "Regional Manager"
    CLUSTER_MANAGER = "cluster_manager", "Cluster Manager"


class User(AbstractUser, AuditLogMixin):
    role = models.CharField(
        max_length=55, choices=RoleChoices.choices, default=RoleChoices.REGIONAL_MANAGER
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    designation = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(blank=True, null=True)
    branch_id = models.IntegerField(null=True, blank=True)
    branch_name = models.CharField(null=True, blank=True, max_length=255)


