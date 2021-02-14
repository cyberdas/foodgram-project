from django.urls import path

from . import views

urlpatterns = [
    path('ingredients/', views.get_ingredients, name='get_ingredients'),
    path('get_wishlist/', views.get_wishlist, name="get_wishlist"),
    path('purchases/', views.add_purchases, name='add_purchases'),
    path('purchases/<int:id>/', views.delete_purchases),
    path('subscriptions/', views.add_subscription, name='add_subscription'),
    path('subscriptions/<int:id>/', views.remove_subscription),
    path('favorites/', views.add_favorite),
    path('favorites/<int:id>/', views.remove_favorite),
]
