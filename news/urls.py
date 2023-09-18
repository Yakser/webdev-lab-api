from django.urls import path

from news.views import (
    NewsDetail,
    NewsList,
    NewsSetViewed,
    CurrentUserNewsList,
    NewsCommentList,
)

app_name = "news"

urlpatterns = [
    path("", NewsList.as_view()),
    path("current/", CurrentUserNewsList.as_view()),
    path("<int:pk>/", NewsDetail.as_view()),
    path("<int:pk>/comments/", NewsCommentList.as_view()),
    path("<int:pk>/set_viewed/", NewsSetViewed.as_view()),
]
