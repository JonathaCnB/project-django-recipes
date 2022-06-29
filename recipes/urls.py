from django.urls import path

from recipes.views.home_recipes import (RecipeDetail, RecipeListViewCategory,
                                        RecipeListViewHome,
                                        RecipeListViewSearch)
from recipes.views.home_recipes_api import RecipeDetailAPI  # noqa
from recipes.views.home_recipes_api import RecipeListViewHomeApi

app_name = "recipes"

urlpatterns = [
    path("", RecipeListViewHome.as_view(), name="home"),
    path("recipes/search/", RecipeListViewSearch.as_view(), name="search"),
    path(
        "recipes/category/<int:category_id>/",
        RecipeListViewCategory.as_view(),
        name="category",
    ),
    path("recipes/<int:pk>/", RecipeDetail.as_view(), name="detail"),
    path(
        "recipes/api/v1/",
        RecipeListViewHomeApi.as_view(),
        name="home_api",
    ),
    path(
        "recipes/api/v1/<int:pk>/",
        RecipeDetailAPI.as_view(),
        name="detail_api",
    ),
]
