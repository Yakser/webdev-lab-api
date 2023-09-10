from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsStaffOrReadOnly
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
        response = super().create(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsDetailSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = News.objects.prefetch_related("comments").all()

    CACHE_KEY_PREFIX = "news_detail"

    @method_decorator(cache_page(60 * 2, key_prefix=CACHE_KEY_PREFIX))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response
