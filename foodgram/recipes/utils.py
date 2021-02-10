def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith("nameIngredient"):
            value_ingredient = key[15:]
            ingredients[request.POST[key]
                        ] = request.POST["valueIngredient_" + value_ingredient]
    return ingredients

def deactivate_tag(request, tag_filters):
    # tag_filters = ["breakfast" и пр]
    if len(tag_filters) > len(set(tag_filters)):
        return list(set(tag_filters))
    return tag_filters
    # удаляет повторные фильтры
    # возращает словарь с уникальными тегами
