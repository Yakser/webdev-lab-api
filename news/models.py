import reprlib

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from core.models import View

User = get_user_model()


class News(models.Model):
    title = models.TextField(
        verbose_name="Заголовок",
    )
    text = models.TextField(
        verbose_name="Текст", help_text="Поддерживается синтаксис Markdown"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="news",
        verbose_name="Автор",
    )
    views = GenericRelation(
        View,
        related_query_name="news_views",
    )
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
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-datetime_created"]

    def __str__(self):
        return f"News<{self.pk}> {reprlib.repr(self.title)}"
