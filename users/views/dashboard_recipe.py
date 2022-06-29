# Flake8: noqa
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from recipes.forms.recipes import UserRecipeForm
from recipes.models import Recipe


class DashboardRecipe(LoginRequiredMixin, View):
    login_url = "users:login"
    redirect_field_name = "next"

    def get_recipe(self, recipe_id):
        recipe = None
        if recipe_id is not None:
            lookup = Q(is_published=False, author=self.request.user, id=recipe_id)
            recipe = get_object_or_404(Recipe, lookup)
        return recipe

    def render_recipe(self, form):
        return render(
            self.request,
            "users/pages/dashboard_recipe.html",
            {"form": form},
        )

    def get(self, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe = self.get_recipe(recipe_id)
        form = UserRecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe_obj = self.get_recipe(recipe_id)
        form = UserRecipeForm(
            self.request.POST or None,
            self.request.FILES or None,
            instance=recipe_obj,
        )
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = self.request.user
            recipe.is_published = False
            recipe.preparation_steps_is_html = False
            recipe.save()

            messages.success(self.request, "Receita atualizada com sucesso.")
            return redirect(reverse("users:recipe_id", args=(recipe.id,)))

        return self.render_recipe(form)


class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe_id = self.request.POST.get("recipe_id")
        recipe_obj = self.get_recipe(recipe_id)
        if recipe_obj:
            recipe_obj.delete()
            messages.success(self.request, "Receita deletada com sucesso.")

        return redirect(reverse("users:dashboard"))
