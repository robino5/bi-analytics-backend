from django.contrib.auth.models import AbstractUser
from django.db import models

from core.mixins import AuditLogMixin

from .managers import BaseUserManager


class RoleChoices(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    MANAGEMENT = "MANAGEMENT", "Management"
    BRANCH_MANAGER = "BRANCH_MANAGER", "Branch Manager"
    REGIONAL_MANAGER = "REGIONAL_MANAGER", "Regional Manager"
    CLUSTER_MANAGER = "CLUSTER_MANAGER", "Cluster Manager"


class User(AbstractUser, AuditLogMixin):
    role = models.CharField(
        max_length=55, choices=RoleChoices.choices, default=RoleChoices.REGIONAL_MANAGER
    )

    objects = BaseUserManager()
    profile: "UserProfile" = models.QuerySet["UserProfile"]

    def is_admin(self) -> bool:
        return self.role == RoleChoices.ADMIN or self.is_superuser or self.is_staff

    def is_branch_manager(self) -> bool:
        return self.role == RoleChoices.BRANCH_MANAGER

    def is_regional_manager(self) -> bool:
        return self.role == RoleChoices.REGIONAL_MANAGER

    def is_cluster_manager(self) -> bool:
        return self.role == RoleChoices.CLUSTER_MANAGER

    def is_management(self) -> bool:
        return self.role == RoleChoices.MANAGEMENT

    def __str__(self) -> str:
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    designation = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(
        blank=True, null=True, verbose_name="Profile Pic", upload_to="profile_images/"
    )
    branch_id = models.IntegerField(null=True, blank=True, verbose_name="Branch Id")
    branch_name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Branch Name"
    )

    def __str__(self) -> str:
        return f"{self.user.username.title()} Profile"


class Trader(models.Model):
    branch_code = models.IntegerField(primary_key=True, db_column="branch_Code")
    branch_name = models.CharField(max_length=255, db_column="branch_Name")
    trader_id = models.CharField(max_length=255, db_column="trader_id")
    trader_name = models.CharField(max_length=255, db_column="trader_name")

    class Meta:
        managed = False
        unique_together = ["branch_code", "trader_id"]
        db_table = "BI_trd_Dealer_info"


class Role(AuditLogMixin):
    codename = models.CharField(max_length=255, unique=True, verbose_name="Code Name")
    viewname = models.CharField(max_length=255, verbose_name="View Name")

    class Meta:
        db_table = "bi_access_role_levels"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.viewname
