from rest_framework import serializers

from comments.models import Comment
from users.serializers import UserListSerializer


class CommentListSerializer(serializers.ModelSerializer):
    author = UserListSerializer()

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "author",  # todo
            "datetime_created",
        ]
