from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from recipes.forms import recipes
from recipes.models import Recipe

from users.forms import LoginForm, RegisterForm


def register(request):
    form_data = request.session.get("register_form_data", None)
    form = RegisterForm(form_data)
    return render(
        request,
        "users/pages/register.html",
        {"form": form, "form_action": reverse("users:register_create")},
    )


def register_create(request):
    if not request.POST:
        raise Http404("Url not found")

    POST = request.POST
    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        data = form.save(commit=False)
        data.set_password(data.password)
        data.username = data.email
        data.save()
        messages.success(request, "Cadastro realizado, por favor faça login.")
        del request.session["register_form_data"]
        return redirect(reverse("users:login"))

    return redirect("users:register")


def login_user(request):
    form_data = request.session.get("login_form_data", None)
    form = LoginForm(form_data)
    return render(
        request,
        "users/pages/login.html",
        {
            "form": form,
            "form_action": reverse("users:login_create"),
        },
    )


def login_create(request):
    if not request.POST:
        raise Http404("Url not found")

    POST = request.POST
    request.session["login_form_data"] = POST
    form = LoginForm(POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),
        )

        if authenticated_user is not None:
            messages.success(request, "Logado com sucesso!")
            login(request, authenticated_user)
        else:
            messages.error(request, "Dados invalidos")
    else:
        messages.error(request, "Error ao validar o formulário")

    return redirect(reverse("users:dashboard"))


@login_required(login_url="users:login", redirect_field_name="next")
def logout_user(request):
    if not request.POST:
        messages.error(request, "Solicitação de logout inválida")
        return redirect(reverse("users:login"))

    if request.POST.get("username") != request.user.username:
        messages.error(request, "Logout de usuário inválido")
        return redirect(reverse("users:login"))

    messages.success(request, "Deslogado com sucesso!")
    logout(request)
    return redirect(reverse("users:login"))


@login_required(login_url="users:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(is_published=False, author=request.user)
    return render(request, "users/pages/dashboard.html", {"recipes": recipes})


@login_required(login_url="users:login", redirect_field_name="next")
def dashboard_recipe_edit(request, recipe_id):
    lookup = Q(is_published=False, author=request.user, id=recipe_id)
    recipe = get_object_or_404(Recipe, lookup)
    form = recipes.UserRecipeForm(
        request.POST or None,
        request.FILES or None,
        instance=recipe,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.is_published = False
        recipe.preparation_steps_is_html = False
        recipe.save()

        messages.success(request, "Receita atualizada com sucesso.")
        return redirect(reverse("users:recipe_id", args=(recipe_id,)))

    return render(
        request,
        "users/pages/dashboard_recipe.html",
        {"recipe": recipe, "form": form},
    )


@login_required(login_url="users:login", redirect_field_name="next")
def dashboard_recipe_create(request):

    form = recipes.UserRecipeForm(
        request.POST or None,
        request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.is_published = False
        recipe.preparation_steps_is_html = False
        recipe.save()

        messages.success(request, "Receita criada com sucesso.")
        return redirect(reverse("users:recipe_id", args=(recipe.id,)))

    return render(
        request,
        "users/pages/dashboard_recipe.html",
        {"form": form, "form_action": reverse("users:recipe_create")},
    )


@login_required(login_url="users:login", redirect_field_name="next")
def dashboard_recipe_delete(request):
    recipe_id = request.POST.get("recipe_id")
    if not request.POST or not recipe_id:
        raise Http404("Url not found")

    lookup = Q(is_published=False, author=request.user, id=recipe_id)

    obj = get_object_or_404(Recipe, lookup)

    obj.delete()

    messages.success(request, "Receita deletada com sucesso.")
    return redirect(reverse("users:dashboard"))
