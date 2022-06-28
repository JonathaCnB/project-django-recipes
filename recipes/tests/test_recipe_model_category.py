from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    def test_category_name_raises_error_if_has_more_than_65_chars(self):
        self.category.name = "a" * 70
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_category_model_string_reprensation(self):
        need = "Test Catgegory Representation"
        self.category.name = need
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), need)
