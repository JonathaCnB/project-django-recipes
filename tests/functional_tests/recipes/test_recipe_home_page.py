from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("Sem receitas cadastras no momento", body.text)

    @patch("recipes.views.PER_PAGES", new=3)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Clique aqui para pesquisar uma receita"]',
        )
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        content_list = self.browser.find_element(
            By.CLASS_NAME,
            "main-content-list",
        )
        self.assertIn("Receita Titulo 0", content_list.text)

    @patch("recipes.views.PER_PAGES", new=3)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        page2 = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Vá para página: 2"]'
        )
        page2.click()
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, "recipe")),
            3,
        )
