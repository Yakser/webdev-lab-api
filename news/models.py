import reprlib

from django.contrib.contenttypes.models import ContentType
from django.db import models


class News(models.Model):
    title = models.TextField(
        verbose_name="Заголовок",
    )
    text = models.TextField(
        verbose_name="Текст",
        help_text="Поддерживается синтаксис Markdown"
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
