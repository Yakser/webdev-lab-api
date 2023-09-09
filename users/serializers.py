from rest_framework import serializers

from news.models import News


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "text",
            "datetime_created",
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "text",
            "datetime_created",
            "datetime_updated",
        ]
