from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response

from . import models
from .models import Country
from .serializers import CountrySerializer
from .tasks import send_telegram_message

def books_view(request):
    return HttpResponse('{"name": "Кобзар"}')


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.annotate(count_selled_books=models.Count('book'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

def create_order(request):

    send_telegram_message.delay(author_id=author_id)