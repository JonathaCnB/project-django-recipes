from unittest.mock import patch

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        resp = self.client.get(reverse("recipes:home"))
        self.assertEqual(resp.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        resp = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(resp, "recipes/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_recipes(self):
        resp = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "Sem receitas cadastras no momento",
            resp.content.decode("utf-8"),
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        resp = self.client.get(reverse("recipes:home"))
        # self.assertEqual(len(resp.context["recipes"]), 1)
        content = resp.content.decode("utf-8")
        context = resp.context["recipes"]
        self.assertIn("user", content)
        self.assertIn("Recipe Title", content)
        self.assertIn("asdasdasdasdasdasdsdasdasd", content)
        self.assertEqual(len(context), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        resp = self.client.get(reverse("recipes:home"))
        content = resp.content.decode("utf-8")
        self.assertIn("<h2>Sem receitas cadastras no momento</h2>", content)

    def test_recipe_home_template_with_pagination(self):
        self.make_recipe_in_batch(9)

        with patch("recipes.views.PER_PAGES", new=3):
            resp = self.client.get(reverse("recipes:home"))
            recipes = resp.context["recipes"]
            paginator = recipes.paginator
            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(9)

        with patch("recipes.views.PER_PAGES", new=3):
            resp = self.client.get(reverse("recipes:home") + "?page=1A")
            self.assertEqual(resp.context["recipes"].number, 1)

            resp = self.client.get(reverse("recipes:home") + "?page=3")
            self.assertEqual(resp.context["recipes"].number, 3)
