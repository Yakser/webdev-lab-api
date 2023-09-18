from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.models import Comment
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

    @method_decorator(cache_page(60 * 2, key_prefix=CACHE_KEY_PREFIX))
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


class CurrentUserNewsList(generics.ListAPIView):
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticated]
    queryset = News.objects.all()

    def get(self, request, *args, **kwargs):
        news = News.objects.filter(author_id=request.user.id)
        news_serialized = NewsListSerializer(news, many=True).data
        return Response(news_serialized, status=status.HTTP_200_OK)


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = News.objects.prefetch_related(
        Prefetch("comments", queryset=Comment.objects.get_moderated())
    ).all()

    CACHE_KEY_PREFIX = "news_detail"

    @method_decorator(cache_page(60 * 2, key_prefix=CACHE_KEY_PREFIX))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
