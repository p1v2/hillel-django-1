from django.http import HttpResponse


def books_view(request):
    return HttpResponse('{"name": "Кобзар"}')
