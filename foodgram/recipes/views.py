from django.shortcuts import render # иморты по pep8
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag, Ingredient, User, Follow, Favorite, WishList
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from .utils import get_ingredients
from django.db.models import Prefetch


def index(request):
    tags_all = Tag.objects.all()
    tag_filters = request.GET.getlist("filters")
    if tag_filters:
        # tag_filters = Tag.objects.filter(slug__in=tag_values)
        recipes = Recipe.objects.filter(tags__slug__in=tag_filters).select_related("author").prefetch_related("tags").distinct()
    else:
        recipes = Recipe.objects.select_related("author").prefetch_related("tags").all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "tags_all": tags_all,
        "tag_filters": tag_filters
    }
    if request.user.is_authenticated:
        wishlist = Recipe.objects.filter(wishlist_recipe__user=request.user).select_related("wishlist_recipe")
        context["wishlist"] = wishlist
    return render(request, 'index.html', context)


@login_required
def feed(request):
    following = User.objects.filter(following__user=request.user).prefetch_related("author_recipes").order_by("id")
    recipes = Recipe.objects.filter(author__following__user=request.user)
    paginator = Paginator(following, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "recipes": recipes,
        "following": following,
        "page": page,
        "paginator": paginator,
    }
    return render(request, "feed.html", context)


@login_required
def new_recipe(request):
    tags = Tag.objects.all() 
    if request.method == "POST":
        form = RecipeForm(request.POST, files=request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            ingredients = get_ingredients(request)
            if not ingredients:
                form.add_error(None, "Добавьте хотя бы один ингредиент")
            else:
                objs = [RecipeIngredient(recipe=new_recipe, amount=value, ingredient=get_object_or_404(Ingredient, title=title))
                    for title, value in ingredients.items()]
                RecipeIngredient.objects.bulk_create(objs)
                form.save_m2m()
                return redirect(reverse('index'))
        return render(request, 'new_recipe.html', {"form": form, "tags": tags})
    form = RecipeForm() 
    return render(request, 'new_recipe.html', {"form": form, "tags": tags})


@login_required # сначала без select_related и prefetch_related
def recipe_edit(request, username, recipe_id):
    user = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe.objects.prefetch_related("tags"), pk=recipe_id)
    tags = Tag.objects.all()
    recipe_tags = recipe.tags.all()
    if request.user != user:
        return redirect('recipe_page', username, recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if request.method == "POST":
        if form.is_valid():
            ingredients = get_ingredients(request)
            if not ingredients:
                form.add_error(None, "Добавьте хотя бы один ингредиент")
            else:
                RecipeIngredient.objects.filter(recipe_id=recipe.id).delete()
                objs = [RecipeIngredient(recipe=recipe, amount=value, ingredient=get_object_or_404(Ingredient, title=title))
                    for title, value in ingredients.items()]
                RecipeIngredient.objects.bulk_create(objs)
                form.save()
                return redirect("recipe_page", username=username, recipe_id=recipe_id)
    context = {
        "form": form,
        "recipe": recipe,
        "tags": tags,
        "recipe_tags": recipe_tags,
    }
    return render(request, "recipe_edit.html", context)


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect("recipe_page", username=username, recipe_id=recipe_id)
    recipe.delete()
    return redirect("profile_page", username=username)


def profile_page(request, username):
    user = get_object_or_404(User, username=username) # user?
    recipes = Recipe.objects.filter(author=user).select_related("author").prefetch_related('tags').order_by("-pub_date")
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "user": user,
    }
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user, author=user).exists()
        favorites = Recipe.objects.filter(favorite_recipe__user=request.user) # recipe=в шаблоне?
        wishlist = Recipe.objects.filter(wishlist_recipe__user=request.user)  
        context["following"] = following
        context["favorites"] = favorites
        context["wishlist"] = wishlist
    return render(request, 'profile_page.html', context)


def recipe_page(request, username, recipe_id): # теги для рецепта
    user = get_object_or_404(User, username=username) # подгрузить ингредиенты
    recipe = get_object_or_404(Recipe.objects.select_related("author").prefetch_related("recipe_ingredients"), pk=recipe_id) # если автор поста - появляется редактировать
    context = {
        "recipe": recipe,
        "user": user,
    }
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user, author=user).exists()
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
        wishlist = WishList.objects.filter(user=request.user, recipe=recipe).exists()
        context["following"] = following
        context["favorite"] = favorite
        context["wishlist"] = wishlist
    return render(request, 'recipe_page.html', context)


@login_required
def favorites(request):
    user = request.user
    recipes = Recipe.objects.filter(favorite_recipe__user=user).select_related("author").prefetch_related("tags")
    wishlist = Recipe.objects.filter(wishlist_recipe__user=user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "wishlist": wishlist,
    }
    return render(request, "favorite.html", context)

@login_required
def get_purchases(request):
    # рецепты, которые добавили в список покупок
    recipes = Recipe.objects.filter(wishlist_recipe__user=request.user, )
    context = {
        "recipes": recipes
    }
    return render(request, "shopList.html", context)


def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
