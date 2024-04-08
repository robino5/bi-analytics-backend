from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Menu


class MenuSerializer(ModelSerializer):
    roles = SerializerMethodField()

    class Meta:
        model = Menu
        fields = "__all__"

    def get_roles(self, instance: Menu):
        return list(instance.roles.values_list("codename", flat=True))
