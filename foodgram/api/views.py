from django.shortcuts import render
from django.http import JsonResponse
from recipes.models import Ingredient, RecipeIngredient
from django.views.decorators.http import require_http_methods


# Create your views here.
@require_http_methods(["GET"])
def get_ingredients(request):
    query = request.GET.get('query')
    ingredients = Ingredient.objects.filter(title__contains=query).values('title','dimension')
    return JsonResponse(list(ingredients), safe=False)