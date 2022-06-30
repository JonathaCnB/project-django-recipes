from django.db.models import F, Q, Value
from django.db.models.aggregates import Count
from django.db.models.functions import Concat
from django.shortcuts import render
from recipes.models import Recipe


def theory(request, *args, **kwargs):
    lookup = Q(id=F("category_id")) | Q(id=F("author_id"))
    recipes = Recipe.objects.filter(lookup).order_by("-id")
    recipes = recipes.annotate(
        author_full_name=Concat(
            F("author__first_name"),
            Value(" "),
            F("author__last_name"),
        ),
    )
    num_of_recipes = Recipe.objects.aggregate(number=Count("id"))

    non_publushed = Recipe.objects.get_non_published()

    # .only() para trazer só os campos selecionados mas não impede de buscar \
    #  outros \

    # .defer() ao contrario do only()

    return render(
        request,
        "theory.html",
        {
            "recipes": recipes,
            "number": num_of_recipes,
            "non_published": non_publushed,
        },
    )
