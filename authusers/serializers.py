from rest_framework.serializers import CharField, ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserProfile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True, allow_null=True, required=False)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "last_login",
        )

    def create(self, validated_data):
        user: User = super().create(validated_data)
        passwd = validated_data.get("password")
        if passwd:
            user.set_password(passwd)
            user.save()
        return user

    def to_representation(self, instance: User):
        data = super().to_representation(instance)
        data["name"] = instance.get_full_name()
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token["username"] = user.username
        token["role"] = user.role

        return token
