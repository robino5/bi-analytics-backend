from datetime import datetime

import django_filters as df
from django.db.models import Q

from .models import User

FILTER_SIGNED_IN_TODAY = (
    ("Yes", "Yes"),
    ("No", "No"),
)


class UserFilter(df.FilterSet):
    branch = df.BaseInFilter(field_name="profile__branch_name", lookup_expr="in")
    role = df.BaseInFilter(field_name="role", lookup_expr="in")
    signedInToday = df.ChoiceFilter(  # noqa: N815
        method="filter_logged_in_today",
        label="Is Logged in Today ?",
        choices=FILTER_SIGNED_IN_TODAY,
    )
    active = df.BooleanFilter(
        method="filter_is_active",
        label="User Status",
    )

    def filter_logged_in_today(self, queryset, _, value):
        today = datetime.today().date()
        users = None
        if value == "Yes":
            users = queryset.filter(last_login__date=today)
        else:
            users = queryset.filter(
                Q(last_login__isnull=True) | Q(last_login__date__lt=today)
            )
        return users

    def filter_is_active(self, queryset, _, value):
        if value is True:
            return queryset.filter(is_active=True)
        return queryset.filter(is_active=False)

    class Meta:
        model = User
        fields = ("username", "email", "active", "role", "branch", "signedInToday")
