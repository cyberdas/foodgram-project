from django.shortcuts import render # иморты по pep8
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag, Ingredient
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from .utils import get_ingredients


def index(request):
    recipes = Recipe.objects.order_by("-pub_date").all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator
    }
    return render(request, 'index.html', context)

@login_required
def new_recipe(request):    
    if request.method == "POST":
        form = RecipeForm(request.POST, files=request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            # new.recipe.tags.add()
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
    tags = Tag.objects.all()
    return render(request, 'new_recipe.html', {"form": form, "tags": tags})