from django.urls import path, include
from . import views

urlpatterns = [
    path('ingredients', views.get_ingredients, name='get_ingredients'),
]