from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from users.forms import UserChangeForm, UserCreationForm
from users.models import Profile, User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ["id", "username", "first_name", "last_name", "email"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ["id", "author", "is_active"]
    list_display_links = ("id", "author")
    search_fields = ["id", "author"]
    list_per_page = 10


# admin.site.unregister(User)
