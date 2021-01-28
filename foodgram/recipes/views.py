from django.shortcuts import render # иморты по pep8
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag, Ingredient, User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from .utils import get_ingredients
from django.db.models import Prefetch


def index(request):
    recipes = Recipe.objects.select_related("author").order_by("-pub_date").all()
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
    tags = Tag.objects.all() 
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
        return render(request, 'new_recipe.html', {"form": form, "tags": tags})
    form = RecipeForm() 
    return render(request, 'new_recipe.html', {"form": form, "tags": tags})


def profile_page(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user).order_by("-pub_date").all()
    # tags = recipes.tags
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "user": user,
        # "tags": tags
    }
    return render(request, 'profile_page.html', context)


def recipe_page(request, username, recipe_id):
    tags = Tag.objects.all()
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user).select_related("author").order_by("-pub_date").all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "tags": tags
    }
        # Recipe.objects.prefetch_related.filter().order_by()
    return render(request, 'recipe_page.html', context)