from django.urls import path

from users import views
from users.views.dashboard_recipe import DashboardRecipe, DashboardRecipeDelete
from users.views.profile import ProfileView

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/create/", views.register_create, name="register_create"),
    path("login/", views.login_user, name="login"),
    path("login/create/", views.login_create, name="login_create"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("logout/", views.logout_user, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "dashboard/recipe/create/",
        DashboardRecipe.as_view(),
        name="recipe_create",
    ),
    path(
        "dashboard/recipe/delete/",
        DashboardRecipeDelete.as_view(),
        name="recipe_delete",
    ),
    path(
        "dashboard/recipe/<int:recipe_id>/edit/",
        DashboardRecipe.as_view(),
        name="recipe_id",
    ),
]
