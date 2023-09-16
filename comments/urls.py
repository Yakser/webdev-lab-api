from django.urls import path

from comments.views import CommentList, UnmoderatedCommentList, UnmoderatedCommentDetail

app_name = "comments"

urlpatterns = [
    path("", CommentList.as_view()),
    path("unmoderated/", UnmoderatedCommentList.as_view()),
    path("unmoderated/<int:pk>/", UnmoderatedCommentDetail.as_view()),
]
