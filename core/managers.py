from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.utils import timezone

from core.constants import VIEWS_CACHING_TIMEOUT

User = get_user_model()


class ViewManager(models.Manager):
    def add_view(self, obj, user):
        obj_type = ContentType.objects.get_for_model(obj)
        view, is_created = self.get_queryset().get_or_create(
            content_type=obj_type, object_id=obj.id, user=user
        )
        return view

    def remove_view(self, obj, user) -> None:
        obj_type = ContentType.objects.get_for_model(obj)
        self.get_queryset().filter(
            content_type=obj_type, object_id=obj.id, user=user
        ).delete()

    def is_viewer(self, obj, user) -> bool:
        if not user.is_authenticated:
            return False
        obj_type = ContentType.objects.get_for_model(obj)
        views = self.get_queryset().filter(
            content_type=obj_type, object_id=obj.id, user=user
        )
        return views.exists()

    def get_viewers(self, obj) -> [User]:
        obj_type = ContentType.objects.get_for_model(obj)
        return User.objects.filter(
            views__content_type=obj_type, views__object_id=obj.id
        )

    def get_views_count(self, obj) -> int:
        obj_type = ContentType.objects.get_for_model(obj)
        # cache this
        views_count = cache.get(f"views_count_{obj_type}_{obj.id}", None)
        if views_count is None:
            views_count = User.objects.filter(
                views__content_type=obj_type, views__object_id=obj.id
            ).count()
            # cache for VIEWS_CACHING_TIMEOUT seconds
            cache.set(
                f"views_count_{obj_type}_{obj.id}", views_count, VIEWS_CACHING_TIMEOUT
            )

        return views_count

    def count_created_last_24_hours(self, obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return (
            self.get_queryset()
            .filter(
                datetime_created__gte=timezone.now() - timedelta(days=1),
                content_type=obj_type,
            )
            .count()
        )
