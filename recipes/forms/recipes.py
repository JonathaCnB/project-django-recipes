from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from utils.django_forms import add_attr
from utils.string import is_positive_number

from recipes.models import Recipe


class UserRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_erros = defaultdict(list)
        add_attr(self.fields.get("preparation_steps"), "class", "span-2")

    class Meta:
        model = Recipe
        exclude = (
            "is_published",
            "slug",
            "author",
            "preparation_steps_is_html",
        )
        widgets = {
            "cover": forms.FileInput(attrs={"class": "span-2"}),
            "servings_unit": forms.Select(
                choices=(
                    ("Porções", "Porções"),
                    ("Pedaços", "Pedaços"),
                    ("Pessoas", "Pessoas"),
                )
            ),
            "preparation_time_unit": forms.Select(
                choices=(
                    ("Minutos", "Minutos"),
                    ("Horas", "Horas"),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get("title")
        if len(title) < 5:
            self._my_erros["title"].append("Deve conter 6 caracteres ou mais.")

        if self._my_erros:
            raise ValidationError(self._my_erros)
        return super_clean

    def clean_preparation_time(self):
        field_name = "preparation_time"
        preparation_time = self.cleaned_data.get(field_name)

        if not is_positive_number(preparation_time):
            self._my_erros[field_name].append("Deve ser maior que 0")

        return preparation_time

    def clean_servings(self):
        field_name = "servings"
        servings = self.cleaned_data.get(field_name)

        if not is_positive_number(servings):
            self._my_erros[field_name].append("Deve ser maior que 0")

        return servings
