from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Tag, Follow

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "dimension", "recipes") 
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
