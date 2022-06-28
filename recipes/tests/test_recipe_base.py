from django.forms import SlugField
from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeMixin:
    def make_category(self, name="Category"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name="user",
        last_name="name",
        username="username",
        password="123456",
        email="u@u.com",
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title: str = "Recipe Title",
        description: str = "asdasdasdasdasdasdsdasdasd",
        slug: SlugField = "one-recipe",
        preparation_time: int = 30,
        preparation_time_unit: str = "Minutos",
        servings: int = 10,
        servings_unit: str = "Pessoas",
        preparation_steps: str = "Isso ai!",
        is_published: bool = True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            is_published=is_published,
        )

    def make_recipe_in_batch(self, qty=18):
        recipes = []
        for i in range(qty):
            kwargs = {
                "title": f"Receita Titulo {i}",
                "slug": f"r{i}",
                "author_data": {
                    "username": f"u{i}",
                    "email": f"t@u{i}.com",
                },
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
