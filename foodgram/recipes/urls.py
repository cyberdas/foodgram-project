from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("feed/", views.FollowListView.as_view(), name="feed"),
    path("favorite/", views.favorites, name="favorites"),
    path("get_purchases/", views.get_purchases, name="get_purchases"),
    path("new_recipe/", views.new_recipe, name="new_recipe"),
    path("<str:username>/", views.profile_page, name="profile_page"),
    path("<str:username>/<int:recipe_id>/", views.recipe_page,
         name="recipe_page"),
    path("<str:username>/<int:recipe_id>/edit/", views.recipe_edit,
         name="recipe_edit"),
    path("<str:username>/<int:recipe_id>/delete/", views.recipe_delete,
         name="recipe_delete"),
]
