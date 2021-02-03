from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from recipes.models import Ingredient, RecipeIngredient, User
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from recipes.models import Follow, User, Favorite, Recipe
import json


# Create your views here.
@require_http_methods(["GET"])
def get_ingredients(request):
    query = request.GET.get('query')
    ingredients = Ingredient.objects.filter(title__contains=query).values('title','dimension')
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
    deleted = Follow.objects.filter(user=request.user, author_id=id).delete()
    return JsonResponse({"success": True})


@require_http_methods(["POST"])
def add_favorite(request): #Добавляем в избранное рецепт
    id = int(json.loads(request.body)["id"])
    user = request.user
    Favorite.objects.get_or_create(user=user, recipe=Recipe.objects.get(pk=id))
    return JsonResponse({"success": True})


@require_http_methods(["DELETE"])
def remove_favorite(request, id):
    user = request.user
    deleted = Favorite.objects.filter(user=user, recipe_id=id).delete()
    return JsonResponse({"success": True})
