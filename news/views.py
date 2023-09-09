from rest_framework import generics

from core.permissions import IsStaffOrReadOnly
from news.models import News
from news.pagination import NewsPagination
from news.serializers import NewsDetailSerializer, NewsListSerializer


class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsListSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = News.objects.all()
    pagination_class = NewsPagination


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsDetailSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = News.objects.all()
