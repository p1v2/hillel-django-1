from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render


def books_view(request):
    return HttpResponse('{"name": "Кобзар"}')


def country_view(request):
    return HttpResponse('{"name": "Ukraine"}')
