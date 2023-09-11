from rest_framework import serializers

from comments.serializers import CommentListSerializer
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
    comments = CommentListSerializer(many=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "text",
            "comments",
            "datetime_created",
            "datetime_updated",
        ]
