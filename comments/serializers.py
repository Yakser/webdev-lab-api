from rest_framework import serializers

from comments.models import Comment


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "author",  # todo
            "datetime_created",
        ]
