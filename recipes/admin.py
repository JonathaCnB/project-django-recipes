"""
    from django.contrib.contenttypes.admin import GenericStackedInline
"""
from django.contrib import admin
from tags.models import Tag

from recipes.models import Category, Recipe

# admin.TabularInline \
# admin.StackedInline
# GenericStackedInline para contenttypes


class TagInline(admin.StackedInline):
    model = Tag
    fields = ("name",)
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ["id", "slug", "author", "category", "is_published"]
    list_display_links = "id", "slug", "author"
    list_editable = ["is_published", "category"]
    search_fields = ["author", "is_published", "category"]
    list_filter = ["author", "is_published", "category"]
    list_per_page = 10
    ordering = ("-id", "author")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("tags",)
    # inlines = [
    #     TagInline,
    # ]


# admin.site.register(Category)
# admin.site.register(Recipe)
# admin.site.unregister(Category)
# admin.site.unregister(Recipe)
