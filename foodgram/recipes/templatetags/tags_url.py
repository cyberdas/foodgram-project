from django import template
from recipes.models import WishList

register = template.Library()


# @register.simple_tag
# def filter_url(request, *args, **kwargs):
    #updated = request.GET.copy()
    #updated.update(kwargs)
    #return updated.urlencode()

@register.filter
def new_filter_link(request, tag):
    # tag = tag.slug
    new_request = request.GET.copy()
    if tag in request.GET.getlist("filters"):
        filters = request.GET.getlist("filters")
        filters.remove(tag)
        new_request.setlist("filters", filters)  # задает значение ключа
    else:
        new_request.appendlist("filters", tag) # добавление значения в ключ filters
    return new_request.urlencode()
