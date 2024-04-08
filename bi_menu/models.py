from django.db import models

from authusers.models import Role
from core.mixins import AuditLogMixin


class Menu(AuditLogMixin):
    codename = models.CharField(max_length=255, verbose_name="Code Name", unique=True)
    viewname = models.CharField(max_length=255, verbose_name="View Name")
    icon = models.TextField(max_length=255, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    roles = models.ManyToManyField(
        Role, related_name="menus", verbose_name="Access Role"
    )
    parent_menu = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="submenus"
    )
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    submenus = models.QuerySet["Menu"]

    class Meta:
        db_table = "bi_menus"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.viewname
