from django.contrib import admin

from recipes.models import Category, Recipe


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


# admin.site.register(Category)
# admin.site.register(Recipe)
# admin.site.unregister(Category)
# admin.site.unregister(Recipe)
