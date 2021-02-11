from .models import Tag


def all_tags(request):
    tags = Tag.objects.all()
    return {"all_tags": tags}
