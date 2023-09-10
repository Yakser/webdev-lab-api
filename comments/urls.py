from django.urls import path

from comments.views import CommentList

app_name = "comments"

urlpatterns = [
    path("", CommentList.as_view()),
]
