from django.shortcuts import render # иморты по pep8
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag, Ingredient
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from .utils import get_ingredients

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
            # new.reciper.tags.add()
            new_recipe.save()
            ingredients = get_ingredients(request)
            # сохраняем каждый ингредиент в рецепт
            objs = [RecipeIngredient(recipe=new_recipe, amount=value, ingredient=get_object_or_404(Ingredient, title=title))
                for title, value in ingredients.items()]
            RecipeIngredient.objects.bulk_create(objs)
            form.save_m2m()
            # add ingredients/tags
            return redirect(reverse('index'))
        return render(request, 'new_recipe.html', {'form': form}) # не проходит валидацию
    form = RecipeForm()
    return render(request, 'new_recipe.html', {"form": form})