from django import forms
from .models import Recipe
from django.forms.widgets import CheckboxSelectMultiple


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'image', 'description', 'cooking_time', 'tags')
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }
