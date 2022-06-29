from django.urls import resolve, reverse
from recipes.views.home_recipes import RecipeListViewCategory

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_by_category_view_function_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func.view_class, RecipeListViewCategory)

    def test_recipe_by_category_view_returns_404_if_no_recipes_found(self):
        resp = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 100}),
        )
        self.assertEqual(resp.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = "This is a category test"
        self.make_recipe(title=needed_title)
        resp = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1}),
        )
        content = resp.content.decode("utf-8")
        context = resp.context["recipes"]
        self.assertIn(needed_title, content)
        self.assertEqual(len(context), 1)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        category_id = recipe.category.id
        resp = self.client.get(
            reverse("recipes:category", kwargs={"category_id": category_id}),
        )
        self.assertEqual(resp.status_code, 404)
