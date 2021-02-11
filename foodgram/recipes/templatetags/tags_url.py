from django import template

register = template.Library()


@register.filter
def new_filter_link(request, tag):
    # tag = tag.slug
    new_request = request.GET.copy()
    if tag in request.GET.getlist("filters"):
        filters = request.GET.getlist("filters")
        filters.remove(tag)
        new_request.setlist("filters", filters)
    else:
        new_request.appendlist("filters", tag)
    return new_request.urlencode()
