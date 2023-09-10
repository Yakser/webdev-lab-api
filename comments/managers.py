from django.db import models


class CommentManager(models.Manager):
    def get_moderated(self):
        return self.get_queryset().filter(is_moderated=True).all()
