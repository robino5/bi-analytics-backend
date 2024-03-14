from django.apps import AppConfig


class AuthusersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authusers"
    verbose_name = "Users Module"

    def ready(self) -> None:
        from . import signals  # noqa: F401
