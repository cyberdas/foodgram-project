from django.urls import path, include
from . import views

urlpatterns = [
    path('ingredients', views.get_ingredients, name='get_ingredients'),
    path('purchases', views.add_purchases, name='add_purchases'),
    path('purchases/<int:id>', views.delete_purchases),
    path('subscriptions', views.add_subscription, name='add_subscription'),
    path('subscriptions/<int:id>', views.remove_subscription),
    path('favorites', views.add_favorite),
    path('favorites/<int:id>', views.remove_favorite),
]