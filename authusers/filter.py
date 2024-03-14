import django_filters as df

from .models import User


class UserFilter(df.FilterSet):
    class Meta:
        model = User
        fields = ("username", "email", "is_active", "role")
