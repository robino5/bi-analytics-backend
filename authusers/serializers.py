from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from .models import User


class UserSerializer(ModelSerializer):
    name = SerializerMethodField()
    password = CharField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "last_login",
        )

    def get_name(self, instance: User) -> str:
        return instance.get_full_name()
