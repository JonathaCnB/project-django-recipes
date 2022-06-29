from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView, ListView
from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGES = settings.PER_PAGES


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    paginate_by = None
    ordering = ["-id"]
    template_name = "recipes/home.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get("recipes"),
            PER_PAGES,
        )
        ctx.update(
            {
                "recipes": page_obj,
                "page_title": "Home",
                "pagination_range": pagination_range,
            }
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/home.html"


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "recipes/home.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs.get("category_id")
        qs = qs.filter(category_id=category_id)
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        recipes = ctx.get("recipes")[0]
        category_title = recipes.category.name
        ctx.update(
            {
                "page_title": f"Categoria {category_title}",
            }
        )
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "recipes/search.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get("q", "").strip()
        if not search_term:
            raise Http404()
        condition_one = Q(title__icontains=search_term)
        condition_two = Q(description__icontains=search_term)
        lookup = Q(condition_one | condition_two)
        qs = qs.filter(lookup)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get("q", "").strip()
        ctx.update(
            {
                "search_term": search_term,
                "page_title": f"Pesquisando por {search_term}",
                "additional_url_query": f"&q={search_term}",
            }
        )
        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/detail.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        recipe = ctx.get("recipe")
        ctx.update(
            {
                "is_detail_page": True,
                "page_title": recipe.slug,
            }
        )
        return ctx
