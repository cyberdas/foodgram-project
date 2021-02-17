from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "image", "description", "cooking_time", "tags")
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }
