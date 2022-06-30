"""
    from django.contrib.contenttypes.fields import GenericRelation
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tags.models import Tag
from users.models import User


class Category(models.Model):
    name = models.CharField("Título", max_length=65)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipes.category"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:category", args=(self.id,))


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True)

    def get_non_published(self):
        return self.filter(is_published=False)


class Recipe(models.Model):
    title = models.CharField("Título", max_length=65)
    description = models.CharField("Descrição", max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.PositiveIntegerField("Tempo de preparação")
    preparation_time_unit = models.CharField("Tempo", max_length=65)
    servings = models.PositiveIntegerField("Serve")
    servings_unit = models.CharField("Únidade", max_length=65)
    preparation_steps = models.TextField("Modo de preparo")
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField("Públicado", default=False)
    cover = models.ImageField(
        "Imagem",
        upload_to="recipes/covers/",
        default="place_holder.png",
        blank=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Autor",
        on_delete=models.SET_NULL,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Categoria",
        on_delete=models.SET_NULL,
        null=True,
    )
    """
        Como fazer relações desacopladas
        tags = GenericRelation(to=Tag, related_query_name="recipes")
    """
    tags = models.ManyToManyField(Tag)

    objects = RecipeManager()

    class Meta:
        db_table = "recipes.recipe"
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:detail", args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = slug

        return super().save(*args, **kwargs)
