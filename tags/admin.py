from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ["id", "slug", "name", "is_active"]
    list_display_links = (
        "id",
        "slug",
    )
    list_editable = ["is_active", "name"]
    search_fields = ["id", "name", "slug"]
    list_per_page = 10
    prepopulated_fields = {
        "slug": ("name",),
    }
