from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = "users.user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users.profile"
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return str(self.author)
