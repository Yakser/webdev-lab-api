from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentListSerializer
from core.models import View
from core.permissions import IsAuthorOrReadOnly
from core.serializers import SetViewedSerializer
from core.utils import delete_cache
from news.models import News
from news.pagination import NewsPagination
from news.serializers import NewsDetailSerializer, NewsListSerializer


class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated]
    queryset = News.objects.all()
    pagination_class = NewsPagination
    CACHE_KEY_PREFIX = "news_list"

    # @method_decorator(cache_page(60 * 2, key_prefix=CACHE_KEY_PREFIX))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        delete_cache(self.CACHE_KEY_PREFIX)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = News.objects.all()

    CACHE_KEY_PREFIX = "news_detail"

    @method_decorator(cache_page(60 * 2, key_prefix=CACHE_KEY_PREFIX))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated]
    queryset = News.objects.all()
    pagination_class = NewsPagination
    CACHE_KEY_PREFIX = "news-viewset"

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "delete"]:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(cache_page(60 * 2, key_prefix=CACHE_KEY_PREFIX))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        delete_cache(self.CACHE_KEY_PREFIX)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response


class NewsSetViewed(generics.GenericAPIView):
    serializer_class = SetViewedSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            news = News.objects.get(pk=self.kwargs["pk"])
            View.objects.add_view(news, request.user)
            return Response(status=status.HTTP_200_OK)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class NewsCommentList(generics.ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()

    CACHE_KEY_PREFIX = "news_comment_list"

    @method_decorator(cache_page(60 * 2, key_prefix=CACHE_KEY_PREFIX))
    def get(self, request, *args, **kwargs):
        try:
            news = News.objects.get(id=kwargs["pk"])
            comments = (
                Comment.objects.get_moderated()
                .select_related("news")
                .filter(news__id=news.id)
            )
            comments_serialized = CommentListSerializer(comments, many=True).data
            return Response(status=status.HTTP_200_OK, data=comments_serialized)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        delete_cache(self.CACHE_KEY_PREFIX)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CurrentUserNewsList(generics.ListAPIView):
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated]
    queryset = News.objects.all()

    def get(self, request, *args, **kwargs):
        news = News.objects.filter(author_id=request.user.id)
        news_serialized = NewsListSerializer(news, many=True).data
        return Response(news_serialized, status=status.HTTP_200_OK)
