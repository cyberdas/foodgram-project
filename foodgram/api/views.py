import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from recipes.models import Follow, Favorite, Recipe, WishList, Ingredient, RecipeIngredient, User


# Create your views here.
@require_http_methods(["GET"])
def get_ingredients(request):
    query = request.GET.get('query')
    ingredients = Ingredient.objects.filter(title__contains=query).values('title', 'dimension')
    return JsonResponse(list(ingredients), safe=False)


@require_http_methods(["POST"])
def add_subscription(request):
    id = int(json.loads(request.body)["id"])
    user = request.user
    if user.id != id:
        _, created = Follow.objects.get_or_create(user=user, author=User.objects.get(pk=id))
        if created:
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@require_http_methods(["DELETE"])
def remove_subscription(request, id):
    Follow.objects.filter(user=request.user, author_id=id).delete()
    return JsonResponse({"success": True})


@require_http_methods(["POST"])
def add_favorite(request):
    id = int(json.loads(request.body)["id"])
    user = request.user
    Favorite.objects.get_or_create(user=user, recipe=Recipe.objects.get(pk=id))
    return JsonResponse({"success": True})


@require_http_methods(["DELETE"])
def remove_favorite(request, id):
    user = request.user
    Favorite.objects.filter(user=user, recipe_id=id).delete()
    return JsonResponse({"success": True})


@require_http_methods(["POST"])
def add_purchases(request):
    user = request.user
    recipe_id = int(json.loads(request.body)["id"])
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    WishList.objects.get_or_create(user=user, recipe_id=recipe_id)
    return JsonResponse({"sucess": True})


@require_http_methods(["DELETE"])
def delete_purchases(request, id):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=id)
    WishList.objects.filter(user=user, recipe=recipe).delete()
    return JsonResponse({"success": True})

@login_required
def get_wishlist(request):
    user = request.user
    recipes = Recipe.objects.filter(wishlist_recipe__user=user)
    ingredients = {}
    ingredients_filter = RecipeIngredient.objects.filter(recipe_id__in=recipes)
    for ingredient in ingredients_filter:
        if ingredient.ingredient in ingredients.keys():
            ingredients[ingredient.ingredient] += ingredient.amount
        else:
            ingredients[ingredient.ingredient] = ingredient.amount
    ingredients_response = []
    for k, v in ingredients.items():
        ingredients_response.append(f"{k.title} ({k.dimension}) — {v} \n")
    response = HttpResponse(ingredients_response, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="ingrediens.txt"'
    return response
