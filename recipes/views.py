from random import randint  # noqa

from django.conf import settings
from django.db.models import Q
from django.http import Http404, HttpResponse  # noqa
from django.shortcuts import get_object_or_404, render
from faker import Faker  # noqa
from utils.pagination import make_pagination

from recipes.models import Category, Recipe, User  # noqa

PER_PAGES = settings.PER_PAGES


def home(request):
    recipes = Recipe.objects.filter(is_published=True)

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGES,
    )

    ctx = {
        "recipes": page_obj,
        "page_title": "Home",
        "pagination_range": pagination_range,
    }
    return render(request, "recipes/home.html", ctx)


def by_category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id)
    recipes = recipes.filter(is_published=True)

    if not recipes:
        raise Http404("Not Found :'(")

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGES,
    )

    category_title = recipes.first().category.name
    ctx = {
        "recipes": page_obj,
        "page_title": f"Categoria {category_title}",
        "pagination_range": pagination_range,
    }
    return render(request, "recipes/home.html", ctx)


def detail(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    ctx = {"recipe": recipe, "is_detail_page": True, "page_title": recipe.slug}
    return render(request, "recipes/detail.html", ctx)


# def create_category(request):
#     for i in range(10):
#         create()
#     return HttpResponse("Criado")


# def create():
#     fake = Faker("pt_BR")
#     cetegory_id = category_rand("category")
#     category = Category.objects.get(id=cetegory_id)
#     Recipe.objects.create(
#         title=fake.sentence(nb_words=6),
#         slug=fake.sentence(nb_words=1),
#         description=fake.sentence(nb_words=12),
#         preparation_time=fake.random_number(digits=2, fix_len=True),
#         preparation_time_unit="Minutos",
#         servings=fake.random_number(digits=2, fix_len=True),
#         servings_unit="Porção",
#         preparation_steps=fake.text(3000),
#         category=category,
#         author=category_rand("user"),
#         is_published=True,
#     )


# def new_author():
#     fake = Faker("pt_BR")
#     first_name = fake.first_name()
#     user = User.objects.create(
#         first_name=first_name,
#         last_name=fake.last_name(),
#         email=fake.email(),
#         username=first_name,
#     )
#     return user


# def category_rand(obj):
#     if obj == "category":
#         return randint(1, 10)
#     id = randint(3, 6)
#     print(id)
#     user = User.objects.get(id=id)
#     return user


def search(request):
    search_term = request.GET.get("q", "").strip()
    if not search_term:
        raise Http404("Not Found :'(")
    condition_one = Q(title__icontains=search_term)
    condition_two = Q(description__icontains=search_term)
    lookup = Q(condition_one | condition_two)
    recipes = Recipe.objects.filter(lookup, is_published=True)
    recipes = recipes.order_by("-id")

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGES,
    )

    ctx = {
        "search_term": search_term,
        "page_title": f"Pesquisando por {search_term}",
        "recipes": page_obj,
        "pagination_range": pagination_range,
        "additional_url_query": f"&q={search_term}",
    }
    return render(request, "recipes/search.html", ctx)
