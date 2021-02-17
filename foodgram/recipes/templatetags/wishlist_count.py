from django import template

from users.models import User

register = template.Library()


@register.filter
def wishlist_count(user):
    result = User.objects.filter(wishlist__user=user).count()
    return result
