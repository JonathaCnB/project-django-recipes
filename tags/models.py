import string
from random import SystemRandom

"""'
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField("Nome", max_length=255)
    slug = models.SlugField(unique=True)
    """
        Como deixar o model sem dependencia
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        object_id = models.CharField("object_id", max_length=255)
        content_object = GenericForeignKey("content_type", "object_id")
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "tags.tag"
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:tags", args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = "".join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            slug = slugify(f"{self.name}-{rand_letters}")
            self.slug = slug

        return super().save(*args, **kwargs)
