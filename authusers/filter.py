from datetime import datetime

import django_filters as df

from .models import User


class UserFilter(df.FilterSet):
    branch = df.BaseInFilter(field_name="profile__branch_name", lookup_expr="in")
    role = df.BaseInFilter(field_name="role", lookup_expr="in")
    signedInToday = df.BooleanFilter(
        method="filter_logged_in_today", label="Is Logged in Today ?"
    )

    def filter_logged_in_today(self, queryset, *args, **kwargs):
        today = datetime.today().date()
        return queryset.filter(last_login__date=today)

    class Meta:
        model = User
        fields = ("username", "email", "is_active", "role", "branch")
