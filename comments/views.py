from rest_framework import generics

from comments.models import Comment
from comments.serializers import CommentsListSerializer
from core.permissions import IsAuthorOrReadOnly


class CommentsList(generics.ListCreateAPIView):
    serializer_class = CommentsListSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    # todo
    # pagination_class = CommentsPagination
