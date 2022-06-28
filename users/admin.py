from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from users.forms import UserChangeForm, UserCreationForm
from users.models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ["id", "username", "first_name", "last_name", "email"]


# admin.site.unregister(User)
