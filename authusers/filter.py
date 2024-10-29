from datetime import datetime

import django_filters as df
from django.db.models import Q

from .models import User


class UserFilter(df.FilterSet):
    branch = df.BaseInFilter(field_name="profile__branch_name", lookup_expr="in")
    role = df.BaseInFilter(field_name="role", lookup_expr="in")
    signedInToday = df.BooleanFilter(
        method="filter_logged_in_today", label="Is Logged in Today ?"
    )

    def filter_logged_in_today(self, queryset, _, value):
        today = datetime.today().date()
        users = None
        if value:
            users = queryset.filter(last_login__date=today)
        else:
            users = queryset.filter(
                Q(last_login__isnull=True) | Q(last_login__date__lt=today)
            )
        return users

    class Meta:
        model = User
        fields = ("username", "email", "is_active", "role", "branch", "signedInToday")
