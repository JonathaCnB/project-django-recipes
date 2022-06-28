from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse("recipes:detail", kwargs={"id": 1}))
        self.assertIs(view.func, views.detail)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        resp = self.client.get(reverse("recipes:detail", kwargs={"id": 100}))
        self.assertEqual(resp.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        needed_title = "This is a detail page - It load one recipe"
        self.make_recipe(title=needed_title)
        resp = self.client.get(
            reverse("recipes:detail", kwargs={"id": 1}),
        )
        content = resp.content.decode("utf-8")
        context = resp.context["recipe"]
        self.assertIn(needed_title, content)
        self.assertEqual(context.id, 1)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        recipe_id = recipe.id
        resp = self.client.get(
            reverse("recipes:detail", kwargs={"id": recipe_id}),
        )
        self.assertEqual(resp.status_code, 404)
