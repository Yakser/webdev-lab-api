from rest_framework import serializers

from news.models import News
from users.serializers import UserListSerializer


class NewsListSerializer(serializers.ModelSerializer):
    author = UserListSerializer(required=False, read_only=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "author",
            "text",
            "datetime_created",
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    author = UserListSerializer(required=False, read_only=True)
    # comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "text",
            "author",
            # "comments",
            "datetime_created",
            "datetime_updated",
        ]
