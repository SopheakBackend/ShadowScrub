from rest_framework import serializers

class SanitizeTextSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, allow_blank=False)
    active_entities = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
        default=None
    )