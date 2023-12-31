from django.contrib import admin
from core.models import View


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "content_type",
        "object_id",
        "content_object",
        "datetime_created",
    )
    list_display_links = (
        "id",
        "user",
        "content_type",
        "object_id",
        "content_object",
        "datetime_created",
    )
    readonly_fields = ("datetime_created",)
