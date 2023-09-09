import reprlib

from django.contrib.auth import get_user_model
from django.db import models

from news.models import News

User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    news = models.ForeignKey(
        News, related_name="comments", on_delete=models.CASCADE, verbose_name="Новость"
    )
    text = models.TextField()
    is_moderated = models.BooleanField(verbose_name="Проверен модератором")
    datetime_created = models.DateTimeField(
        verbose_name="Дата создания",
        null=False,
        auto_now_add=True,
    )
    datetime_updated = models.DateTimeField(
        verbose_name="Дата изменения",
        null=False,
        auto_now=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["datetime_created"]  # todo

    def __str__(self):
        return f"Comment<{self.pk}> {reprlib.repr(self.text)}"
