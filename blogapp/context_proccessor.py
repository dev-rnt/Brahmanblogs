from .models import Categories


def cat_links(request):
    links = Categories.objects.all()
    return dict(links=links)


    