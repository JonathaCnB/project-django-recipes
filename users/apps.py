from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Usuarios"

    def ready(self, *args, **kwargs):
        import users.signals  # noqa

        return super().ready(*args, **kwargs)
