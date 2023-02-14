from django.db.models import Count, Avg, Sum, Subquery
from rest_framework.viewsets import ModelViewSet

from books.models import Book, Author, Country
from books.serializers import BookSerializer, AuthorSerializer, CountrySerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().select_related('country').prefetch_related('authors')
    serializer_class = BookSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().annotate(books_count=Count('book'), average_price=Avg('book__price'))
    serializer_class = AuthorSerializer

# У CoutryViewset додати через annotate поле count_selled_books, де порахувати кількість проданих книжок по кожній країні.
class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all().annotate(count_selled_books=Sum('book__count_selled'))
    serializer_class = CountrySerializer
