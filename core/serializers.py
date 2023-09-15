from rest_framework import serializers


class SetViewedSerializer(serializers.Serializer):
    is_viewed = serializers.BooleanField(required=True)
