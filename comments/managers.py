from datetime import timedelta

from django.db import models
from django.utils import timezone


class CommentManager(models.Manager):
    def get_moderated(self):
        return self.get_queryset().filter(is_moderated=True).all()

    def count_created_last_24_hours(self):
        return (
            self.get_queryset()
            .filter(datetime_created__gte=timezone.now() - timedelta(days=1))
            .count()
        )
