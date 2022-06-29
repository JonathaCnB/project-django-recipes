from django.forms.models import model_to_dict
from django.http import JsonResponse

from .home_recipes import RecipeDetail, RecipeListViewBase


class RecipeListViewHomeApi(RecipeListViewBase):
    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()["recipes"]
        recipes_list = list(recipes.object_list.values())
        return JsonResponse(
            {"recipes": recipes_list},
            safe=False,
            json_dumps_params={"indent": 4},
        )


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()["recipe"]
        recipe_dict = model_to_dict(recipe)
        absolute_url = self.request.build_absolute_uri()

        if recipe_dict.get("cover"):
            recipe_dict["cover"] = absolute_url + recipe_dict["cover"].url[1:]
        else:
            recipe_dict["cover"] = ""

        recipe_dict["created_at"] = str(recipe.created_at)
        recipe_dict["updated_at"] = str(recipe.updated_at)
        recipe_dict["get_absolute_url"] = str(absolute_url)

        return JsonResponse(
            {"recipe": recipe_dict},
            safe=False,
            json_dumps_params={"indent": 4},
        )
