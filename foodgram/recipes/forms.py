from django import forms
from .models import Recipe, RecipeIngredient, Tag, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model= Recipe
        fields = ('title', 'image', 'description', 'cooking_time')
        # exclude = ('tags', 'ingredients')