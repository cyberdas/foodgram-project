from django import template
from recipes.models import WishList

register = template.Library()


@register.simple_tag
def filter_url(request, *args, **kwargs):
    updated = request.GET.copy()
    updated.update(kwargs)
    return updated.urlencode()
