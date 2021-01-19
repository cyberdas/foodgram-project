from django.shortcuts import render
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag, Ingredient

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def new_recipe(request):
    return render(request, 'formRecipe.html', {})
    