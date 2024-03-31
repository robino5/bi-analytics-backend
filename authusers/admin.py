from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    admin.site.site_header = "📊 BI Analytics"
    admin.site.site_title = "BI Analytics - LBSL"
    # Define the fields to be displayed in the user list in the admin panel
    list_display = (
        "name",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    # Define the fields to be used in the user creation and editing form in the admin
    # panel
    fieldsets = (
        (
            "🙎‍♂️ Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        (
            "🔐 Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Metrics",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                )
            },
        ),
    )
    # Define the fields to be used in the add user form in the admin panel
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "role", "password1", "password2"),
            },
        ),
    )
    # Define the search fields to be used in the admin panel's search bar
    search_fields = ("name", "username", "first_name", "last_name", "email")
    # Define the ordering of the users in the admin panel
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    search_fields = ("username", "first_name", "last_name", "email")
    inlines = (ProfileInline,)

    def name(self, instance: User, **kwargs):
        return instance.get_full_name()
