from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "is_moderated",
        "datetime_created",
        "datetime_updated",
    )
    list_display_links = (
        "id",
        "text",
        "is_moderated",
        "datetime_created",
        "datetime_updated",
    )
    list_filter = (
        "datetime_created",
        "datetime_updated",
    )
    search_fields = ("text",)
    readonly_fields = (
        "datetime_created",
        "datetime_updated",
    )
    ordering = ("is_moderated", "-datetime_created")
