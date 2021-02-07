from django import template
from recipes.models import WishList

register = template.Library()


@register.filter
def wishlist_count(user):
    result = WishList.objects.filter(user=user).count()
    return result
