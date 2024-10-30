from typing import Any

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from bi_menu.models import Menu

from .models import Role, UserProfile

UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "👤 Profile"


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    admin.site.site_header = "📊 BI Analytics"
    admin.site.site_title = "BI Analytics - LBSL"
    list_display_links = ("name", "username")
    # Define the fields to be displayed in the user list in the admin panel
    list_display = (
        "name",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = ("role", "is_active")
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
                    "role_fk",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "⚙️ Important Metrics",
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
    inlines = [ProfileInline]
    list_per_page = 15

    def name(self, instance, **kwargs):
        return instance.get_full_name()


class UserInline(admin.TabularInline):
    model = UserModel
    show_change_link = True
    can_delete = True
    fields = ["username", "is_active"]
    extra = 0
    readonly_fields = ["username", "is_active"]


class MenuInline(admin.TabularInline):
    model = Menu.roles.through
    extra = 0


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("codename", "viewname")
    search_fields = ("codename", "viewname")

    inlines = [UserInline, MenuInline]
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
