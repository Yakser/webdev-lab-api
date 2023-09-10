from rest_framework import serializers

from comments.models import Comment
from comments.service import notify_moderators_about_new_comment
from users.serializers import UserListSerializer


class CommentListSerializer(serializers.ModelSerializer):
    author = UserListSerializer(required=False, read_only=True)

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.save()
        author_fullname = f"{comment.author.first_name} {comment.author.last_name}"
        notify_moderators_about_new_comment.delay(author_fullname, comment.pk)
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
