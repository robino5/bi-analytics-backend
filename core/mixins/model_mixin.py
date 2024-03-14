from django.conf import settings
from django.db import models

__all__ = ["TimestampedMixin", "UserTrackedMixin", "AuditLogMixin"]


class TimestampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserTrackedMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_by_%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_by_%(class)s_related",
    )

    class Meta:
        abstract = True


class AuditLogMixin(TimestampedMixin, UserTrackedMixin):
    class Meta:
        abstract = True
