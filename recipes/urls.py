from django.urls import path

from recipes import views

app_name = "recipes"

urlpatterns = [
    path("", views.home, name="home"),
    # path("create/", views.create_category, name="create"),
    path("recipes/search/", views.search, name="search"),
    path(
        "recipes/category/<int:category_id>/",
        views.by_category,
        name="category",
    ),
    path("recipes/<int:id>/", views.detail, name="detail"),
]
