from django.shortcuts import render # иморты по pep8
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag, Ingredient
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

@login_required
def new_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            # add ingredients/tags
            form.save_m2m()
            return redirect(reverse('index'))
    form = RecipeForm()
    return render(request, 'new_recipe.html', {"form": form})