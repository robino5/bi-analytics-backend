from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Menu


class MenuSerializer(ModelSerializer):
    roles = SerializerMethodField()
    submenus = SerializerMethodField()

    class Meta:
        model = Menu
        exclude = ("created_at", "created_by", "updated_at", "updated_by")

    def get_roles(self, instance: Menu):
        return list(instance.roles.values_list("codename", flat=True))

    def get_submenus(self, obj: Menu):
        submenus = obj.submenus.prefetch_related("submenus").all()
        serialized = self.__class__(submenus, many=True)
        return serialized.data
