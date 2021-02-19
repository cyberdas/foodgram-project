from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from foodgram.settings import items_for_pagination
from users.models import User

from .forms import RecipeForm
from .models import (Favorite, Follow, Recipe, RecipeIngredient,
                     WishList)
from .utils import get_ingredients, save_recipe, get_recipes


def index(request):
    tag_filters, recipes = get_recipes(request)
    paginator = Paginator(recipes, items_for_pagination)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "tag_filters": tag_filters
    }
    if request.user.is_authenticated:
        wishlist = Recipe.objects.filter(wishlist_recipe__user=request.user)
        context["wishlist"] = wishlist
    return render(request, "index.html", context)


@login_required
def feed(request):
    following = User.objects.filter(
        following__user=request.user).prefetch_related(
        "author_recipes").order_by("id")
    recipes = Recipe.objects.filter(author__following__user=request.user)
    paginator = Paginator(following, items_for_pagination)
    page_number = request.GET.get("page")
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
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_recipe = form.save(commit=False)
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, "Добавьте хотя бы один ингредиент")
        else:
            save_recipe(request, ingredients, new_recipe)
            return redirect(reverse("index"))
    return render(request, "new_recipe.html", {"form": form})


@login_required
def recipe_edit(request, username, recipe_id):
    user = get_object_or_404(User, username=username)
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related("tags"), pk=recipe_id)
    recipe_tags = recipe.tags.all()
    if request.user != user:
        return redirect("recipe_page", username, recipe_id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)
    if form.is_valid():
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, "Добавьте хотя бы один ингредиент")
        else:
            RecipeIngredient.objects.filter(recipe_id=recipe.id).delete()
            new_recipe = form.save(commit=False)
            save_recipe(request, ingredients, new_recipe)
            form.save()
            return redirect("recipe_page", username=username,
                            recipe_id=recipe_id)
    context = {
        "form": form,
        "recipe": recipe,
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
    user = get_object_or_404(User, username=username)
    tag_filters, recipes = get_recipes(request, user=user)
    paginator = Paginator(recipes, items_for_pagination)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "user": user,
        "tag_filters": tag_filters,
    }
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=user).exists()
        favorites = Recipe.objects.filter(favorite_recipe__user=request.user)
        wishlist = Recipe.objects.filter(wishlist_recipe__user=request.user)
        context["following"] = following
        context["favorites"] = favorites
        context["wishlist"] = wishlist
    return render(request, "profile_page.html", context)


def recipe_page(request, username, recipe_id):
    user = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe.objects.select_related(
        "author").prefetch_related(
        "recipe_ingredients"), pk=recipe_id, author=user)
    context = {
        "recipe": recipe,
    }
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=recipe.author).exists()
        favorite = Favorite.objects.filter(
            user=request.user, recipe=recipe).exists()
        wishlist = WishList.objects.filter(
            user=request.user, recipe=recipe).exists()
        context["following"] = following
        context["favorite"] = favorite
        context["wishlist"] = wishlist
    return render(request, "recipe_page.html", context)


@login_required
def favorites(request):
    favorite_user = request.user
    tag_filters, recipes = get_recipes(request, favorite_user=favorite_user)
    wishlist = Recipe.objects.filter(wishlist_recipe__user=favorite_user)
    paginator = Paginator(recipes, items_for_pagination)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "wishlist": wishlist,
        "tag_filters": tag_filters,
    }
    return render(request, "favorite.html", context)


@login_required
def get_purchases(request):
    """Рецепты, которые добавили в список покупок"""
    recipes = Recipe.objects.filter(wishlist_recipe__user=request.user, )
    context = {
        "recipes": recipes
    }
    return render(request, "shopList.html", context)
