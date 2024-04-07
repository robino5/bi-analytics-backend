from django.contrib import admin

# Register your models here.
from .models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("codename", "viewname", "path", "parent_menu", "is_active")
    search_fields = ("codename", "viewname", "path")
    list_filter = ("is_active", "roles")
