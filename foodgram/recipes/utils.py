from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith("nameIngredient"):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                "valueIngredient_" + value_ingredient]
    return ingredients


def save_recipe(request, ingredients, new_recipe):
    new_recipe.author = request.user
    new_recipe.save()
    objs = [RecipeIngredient(recipe=new_recipe, amount=value,
            ingredient=get_object_or_404(Ingredient, title=title))
            for title, value in ingredients.items()]
    RecipeIngredient.objects.bulk_create(objs)
