from enum import Enum

import django_filters as df
from django.db.models import Q, QuerySet
from django.utils import timezone

from .models import User


class FilterChioces(Enum):
    YES = "Yes"
    NO = "No"


FILTER_SIGNED_IN_TODAY = (
    (FilterChioces.YES.value, FilterChioces.YES.value),
    (FilterChioces.NO.value, FilterChioces.NO.value),
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

    def filter_logged_in_today(self, queryset: QuerySet, _, value: str) -> QuerySet:
        """
        Filter users based on their login status for the current day.

        Args:
            queryset: The base queryset to filter
            value: 'Yes' or 'No' indicating whether to filter for logged in users

        Returns:
            Filtered queryset based on login status
        """
        today = timezone.now().date()
        if value == FilterChioces.YES.value:
            return queryset.filter(last_login__date=today)
        return queryset.filter(
            Q(last_login__isnull=True) | Q(last_login__date__lt=today)
        )

    def filter_is_active(self, queryset: QuerySet, _, value: bool) -> QuerySet:
        return queryset.filter(is_active=value)

    class Meta:
        model = User
        fields = ("username", "email", "active", "role", "branch", "signedInToday")
