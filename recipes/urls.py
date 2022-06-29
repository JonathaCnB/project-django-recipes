from django.urls import path

from recipes.views.home_recipes import (
    RecipeDetail,
    RecipeListViewCategory,
    RecipeListViewHome,
    RecipeListViewSearch,
)

app_name = "recipes"

urlpatterns = [
    path("", RecipeListViewHome.as_view(), name="home"),
    # path("create/", views.create_category, name="create"),
    path("recipes/search/", RecipeListViewSearch.as_view(), name="search"),
    path(
        "recipes/category/<int:category_id>/",
        RecipeListViewCategory.as_view(),
        name="category",
    ),
    path("recipes/<int:pk>/", RecipeDetail.as_view(), name="detail"),
]
