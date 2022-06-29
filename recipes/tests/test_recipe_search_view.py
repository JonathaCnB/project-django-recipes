from django.urls import resolve, reverse
from recipes.views.home_recipes import RecipeListViewSearch

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_user_correct_view_function(self):
        resolved = resolve(reverse("recipes:search"))
        self.assertIs(resolved.func.view_class, RecipeListViewSearch)

    def test_recipe_search_loads_correct_template(self):
        resp = self.client.get(reverse("recipes:search") + "?q=Search")
        self.assertTemplateUsed(resp, "recipes/search.html")
        self.assertEqual(resp.status_code, 200)

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse("recipes:search")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse("recipes:search") + '?q="<Search>"'
        resp = self.client.get(url)
        content = resp.content.decode("utf-8")
        self.assertIn("Pesquisando por &quot;&lt;Search&gt;&quot;", content)

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = "This is recipe one"
        title2 = "This is recipe two"
        title3 = "This is recipe tree"

        recipe1 = self.make_recipe(
            title=title1,
            slug="one",
            author_data={"username": "one"},
        )
        recipe2 = self.make_recipe(
            title=title2,
            slug="two",
            author_data={"username": "two"},
        )
        recipe3 = self.make_recipe(
            description=title3,
            slug="tree",
            author_data={"username": "tree"},
        )

        search_url = reverse("recipes:search")
        resp1 = self.client.get(f"{search_url}?q={title1}")
        resp2 = self.client.get(f"{search_url}?q={title2}")
        resp_both = self.client.get(f"{search_url}?q=this")
        content1 = resp1.content.decode("utf-8")
        content2 = resp2.content.decode("utf-8")
        self.assertIn(recipe1, resp1.context["recipes"])
        self.assertNotIn(title2, content1)
        self.assertIn(recipe2, resp2.context["recipes"])
        self.assertIn(title2, content2)
        self.assertIn(recipe1, resp_both.context["recipes"])
        self.assertIn(recipe2, resp_both.context["recipes"])
        self.assertIn(recipe3, resp_both.context["recipes"])
