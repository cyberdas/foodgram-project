from django import forms
from .models import Recipe, RecipeIngredient, Tag, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model= Recipe
        fields = ('title', 'tags', 'image', 'ingredients', 'description', 'cooking_time', 'slug')
        # exclude = ('tags', 'ingredients')