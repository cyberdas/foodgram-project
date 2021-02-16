import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, WishList)
from users.models import User


@require_http_methods(["GET"])
def get_ingredients(request):
    query = request.GET.get('query')
    ingredients = Ingredient.objects.filter(title__contains=query).values(
        'title', 'dimension')
    return JsonResponse(list(ingredients), safe=False)


@require_http_methods(["POST"])
def add_subscription(request):
    body = json.loads(request.body)
    author_id = body.get("id", None)
    author = get_object_or_404(User, pk=author_id)
    user = request.user
    if author != user:
        obj, created = Follow.objects.get_or_create(
            user=user, author=author)
        return JsonResponse({"success": created})
    return JsonResponse({"success": False})


@require_http_methods(["DELETE"])
def remove_subscription(request, author_id):
    author = get_object_or_404(User, pk=author_id)
    if request.user != author:
        subscription = get_object_or_404(
            Follow, user=request.user, author=author)
        subscription.delete()
        return JsonResponse({'success': True})
    return JsonResponse({"success": False})


@require_http_methods(["POST"])
def add_favorite(request):
    body = json.loads(request.body)
    recipe_id = body.get("id", None)
    if recipe_id:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        obj, created = Favorite.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse({"success": created})
    return JsonResponse({"success": False})


@require_http_methods(["DELETE"])
def remove_favorite(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Favorite, user=user, recipe_id=recipe_id)
    recipe.delete()
    return JsonResponse({"success": True})


@require_http_methods(["POST"])
def add_purchases(request):
    user = request.user
    body = json.loads(request.body)
    recipe_id = body.get("id", None)
    if recipe_id:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        obj, created = WishList.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse({"success": created})
    return JsonResponse({"success": False})


@require_http_methods(["DELETE"])
def delete_purchases(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_wishlist = get_object_or_404(WishList, user=user, recipe=recipe)
    recipe_wishlist.delete()
    return JsonResponse({"success": True})


@login_required
def get_wishlist(request):
    user = request.user
    recipes = Recipe.objects.filter(wishlist_recipe__user=user)
    ingredients = {}
    ingredients_filter = RecipeIngredient.objects.filter(recipe_id__in=recipes)
    for ingredient in ingredients_filter:
        if ingredient.ingredient in ingredients:
            ingredients[ingredient.ingredient] += ingredient.amount
        else:
            ingredients[ingredient.ingredient] = ingredient.amount
    ingredients_response = []
    for k, v in ingredients.items():
        ingredients_response.append(f"{k.title} ({k.dimension}) - {v} \n")
    response = HttpResponse(ingredients_response, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="ingrediens.txt"'
    return response
