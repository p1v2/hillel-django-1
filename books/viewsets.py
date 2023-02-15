from django.db.models import Count, Avg
from rest_framework.viewsets import ModelViewSet

from books.models import Book, Author
from books.serializers import BookSerializer, AuthorSerializer, CountrySerializer
from hillel_django.permissions import IsSellerOrAdminOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('country').prefetch_related('authors')

    serializer_class = BookSerializer
    permission_classes = [IsSellerOrAdminOrReadOnly]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().annotate(books_count=Count('book'), average_price=Avg('book__price'))
    serializer_class = AuthorSerializer


class CountryViewSet(ModelViewSet):
    pass
    serializer_class = CountrySerializer
