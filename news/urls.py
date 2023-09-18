from django.urls import path
from rest_framework.routers import DefaultRouter

from news.views import (
    # NewsDetail,
    # NewsList,
    NewsSetViewed,
    CurrentUserNewsList,
    NewsCommentList,
    NewsViewSet,
)

app_name = "news"
router = DefaultRouter()
router.register("", NewsViewSet, basename="news")


urlpatterns = [
    # path("", NewsList.as_view()),
    path("current/", CurrentUserNewsList.as_view()),
    # path("<int:pk>/", NewsDetail.as_view()),
    path("<int:pk>/comments/", NewsCommentList.as_view()),
    path("<int:pk>/set_viewed/", NewsSetViewed.as_view()),
] + router.urls
