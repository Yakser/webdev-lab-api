from django.contrib import admin

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "text",
        "datetime_created",
        "datetime_updated",
    )
    list_display_links = (
        "id",
        "title",
        "text",
        "datetime_created",
        "datetime_updated",
    )
    list_filter = (
        "datetime_created",
        "datetime_updated",
    )
    search_fields = ("title", "text",)
    readonly_fields = (
        "datetime_created",
        "datetime_updated",
    )
