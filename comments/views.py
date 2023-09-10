from rest_framework import generics

from comments.models import Comment
from comments.serializers import CommentListSerializer
from core.permissions import IsAuthorOrReadOnly


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    # todo
    # pagination_class = CommentsPagination
