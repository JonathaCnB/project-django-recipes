from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = "users.user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
