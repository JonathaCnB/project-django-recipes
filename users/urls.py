from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/create/", views.register_create, name="register_create"),
    path("login/", views.login_user, name="login"),
    path("login/create/", views.login_create, name="login_create"),
    path("logout/", views.logout_user, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "dashboard/recipe/create/",
        views.dashboard_recipe_create,
        name="recipe_create",
    ),
    path(
        "dashboard/recipe/delete/",
        views.dashboard_recipe_delete,
        name="recipe_delete",
    ),
    path(
        "dashboard/recipe/<int:recipe_id>/edit/",
        views.dashboard_recipe_edit,
        name="recipe_id",
    ),
]
