from rest_framework import generics, status
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentListSerializer
from core.permissions import IsAuthorOrReadOnly


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.get_moderated()

    # todo
    # pagination_class = CommentsPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# todo: set_moderated view
