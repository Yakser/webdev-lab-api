from rest_framework import serializers

from comments.models import Comment
from comments.service import notify_moderators_about_new_comment
from users.serializers import UserListSerializer


class CommentListSerializer(serializers.ModelSerializer):
    author = UserListSerializer(required=False, read_only=True)

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.save()
        notify_moderators_about_new_comment(comment)
        return comment

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "author",  # todo
            "news",
            "datetime_created",
        ]

        extra_kwargs = {"author": {"read_only": True}}
