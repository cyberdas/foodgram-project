from django import template
from recipes.models import Tag
register = template.Library()


@register.filter 
def addclass(field, css):
        return field.as_widget(attrs={"class": css})

@register.filter
def all_tags(value):
    """Возвращает все теги."""

    return Tag.objects.all()