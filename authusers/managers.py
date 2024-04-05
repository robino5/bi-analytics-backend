from typing import Iterable

from django.contrib.auth.models import BaseUserManager as UserManager
from django.db.models.signals import post_save


class BaseUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The username field must be set.")

        if not password:
            raise ValueError("The Password field must be set.")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "REGIONAL_MANAGER")
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")

        return self._create_user(username, password, **extra_fields)

    def create_staff_user(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def bulk_create(
        self,
        objs: Iterable,
        batch_size: int | None = None,
        **kwargs,
    ) -> list:
        created_users = super().bulk_create(
            objs,
            batch_size,
        )
        for user in objs:
            post_save.send(user.__class__, instance=user, created=True)

        return created_users
