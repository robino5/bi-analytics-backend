from django.contrib.auth.models import AbstractUser
from django.db import models

from core.mixins import AuditLogMixin

from .managers import BaseUserManager


class Role(AuditLogMixin):
    codename = models.CharField(max_length=255, unique=True, verbose_name="Code Name")
    viewname = models.CharField(max_length=255, verbose_name="View Name")

    class Meta:
        db_table = "bi_access_role_levels"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.viewname


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

    role_fk = models.ForeignKey(
        Role, on_delete=models.SET_NULL, related_name="role_users", null=True
    )

    objects = BaseUserManager()
    profile: "UserProfile" = models.QuerySet["UserProfile"]
    board_permissions: "BoardPermission" = models.QuerySet["BoardPermission"]
    
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


class BoardPermission(models.Model):
    active_trading_codes = models.BooleanField(default=False)
    business_and_trade_management = models.BooleanField(default=False)
    trade_insights = models.BooleanField(default=False)
    customer_management = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="board_permissions")

    class Meta:
        db_table = "board_permission"  

    def __str__(self):
        return f"{self.user.username.title()} Board Permissions"


class Trader(models.Model):
    branch_code = models.IntegerField(primary_key=True, db_column="branch_Code")
    branch_name = models.CharField(max_length=255, db_column="branch_Name")
    trader_id = models.CharField(max_length=255, db_column="trader_id")
    trader_name = models.CharField(max_length=255, db_column="trader_name")

    class Meta:
        managed = False
        unique_together = ["branch_code", "trader_id"]
        db_table = "BI_trd_Dealer_info"
