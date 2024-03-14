from django.db.models import TextChoices
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers


class StatusChoices(TextChoices):
    SUCCESS = "success"
    FAILED = "failure"


class EmptySerializer(serializers.Serializer):
    pass


def enveloper(serializer_class: serializers.Serializer, many: bool):
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
