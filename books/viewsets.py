from django.db.models import Count, Avg
from rest_framework.viewsets import ModelViewSet

from books.models import Book, Author
from books.serializers import BookSerializer, AuthorSerializer
from hillel_django.permissions import IsSellerOrAdminOrReadOnly

from rest_framework import viewsets
from .models import Country
from .serializers import CountrySerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.filter(archived=False)

    serializer_class = BookSerializer
    permission_classes = [IsSellerOrAdminOrReadOnly]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().annotate(books_count=Count('book'), average_price=Avg('book__price'))
    serializer_class = AuthorSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
