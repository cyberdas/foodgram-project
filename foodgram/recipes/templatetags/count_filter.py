from django import template

register = template.Library()


@register.filter
def count_filter(value):
    result = value - 3
    return result