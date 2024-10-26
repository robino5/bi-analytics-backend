from typing import Type

from django.db.models import TextChoices
from drf_spectacular.utils import extend_schema_serializer
from pydantic import BaseModel
from rest_framework import serializers


class StatusChoices(TextChoices):
    SUCCESS = "success"
    FAILED = "failure"


class EmptySerializer(serializers.Serializer):
    pass


def enveloper(serializer_class: Type[serializers.BaseSerializer], many: bool):
    component_name = "Enveloped{}{}".format(
        serializer_class.__name__.replace("Serializer", ""),
        "List" if many else "",
    )

    @extend_schema_serializer(many=False, component_name=component_name)
    class EnvelopeSerializer(serializers.Serializer):
        status = serializers.ChoiceField(choices=StatusChoices.choices)
        code = serializers.IntegerField(help_text="Valid HTTP status code")
        data = serializer_class(many=many)
        message = serializers.CharField(allow_null=True, required=False)

    return EnvelopeSerializer


def pydantic_enveloper(model_class: Type[BaseModel], many: bool):
    component_name = f"Enveloped{model_class.__name__}{'List' if many else ''}"

    @extend_schema_serializer(many=False, component_name=component_name)
    class EnvelopeSerializer(serializers.Serializer):
        status = serializers.ChoiceField(
            choices=[("success", "Success"), ("error", "Error")]
        )
        code = serializers.IntegerField(help_text="Valid HTTP status code")
        data = serializers.ListField(
            child=serializers.DictField(),
            required=True,
            allow_empty=many,
        )
        message = serializers.CharField(allow_null=True, required=False)

    return EnvelopeSerializer
