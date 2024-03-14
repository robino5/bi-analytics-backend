from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token["username"] = user.username
        token["role"] = user.role

        return token
