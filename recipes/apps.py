from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"
    verbose_name = "Receitas"

    def ready(self, *args, **kwargs):
        import recipes.signals  # noqa

        return super().ready(*args, **kwargs)
