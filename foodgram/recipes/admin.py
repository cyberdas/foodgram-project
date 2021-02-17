from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, Recipe, RecipeIngredient,
                     Tag, WishList)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "dimension")
    empty_value_display = "-пусто-"
    search_fields = ("title",)
    list_filter = ("title", )


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ("title", "author", )
    list_filter = ("title", )


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


class WishListAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(WishList, WishListAdmin)
