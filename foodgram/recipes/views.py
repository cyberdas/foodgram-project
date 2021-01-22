from django.shortcuts import render # иморты по pep8
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag, Ingredient
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

@login_required
def new_recipe(request):    
    if request.method == "POST":
        form = RecipeForm(request.POST, files=request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            ingredients = request.POST.getlist('nameIngredient')
            print('krappa')
            # add ingredients/tags
            return redirect(reverse('index'))
        return render(request, 'new_recipe.html', {'form': form}) # не проходит валидацию
    form = RecipeForm()
    return render(request, 'new_recipe.html', {"form": form})