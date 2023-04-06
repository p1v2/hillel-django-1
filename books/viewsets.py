from django.core.cache import cache
from django.db.models import Count, Avg
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from books.models import Book, Author, Order, Country
from books.pagination import BookPagination, SomeCustomPagination
from books.serializers import BookSerializer, AuthorSerializer, OrderSerializer, CountrySerializer
from hillel_django.permissions import IsSellerOrAdminOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('country').prefetch_related('authors')

    serializer_class = BookSerializer
    permission_classes = [IsSellerOrAdminOrReadOnly]
    pagination_class = BookPagination

    def list(self, request, *args, **kwargs):
        # Check if books are cached
        get_args = request.GET.dict()
        books = cache.get(f"books:{get_args}")
        if books:
            return Response(books)

        response = super().list(request, *args, **kwargs)

        cache.set(f"books:{get_args}", response.data)

        return response

    def retrieve(self, request, *args, **kwargs):
        # Check if book is cached
        book = cache.get(f"book:{kwargs['pk']}")
        if book:
            return Response(book)

        response = super().retrieve(request, *args, **kwargs)

        cache.set(f"book:{kwargs['pk']}", response.data)

        return response


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().annotate(books_count=Count('books'), average_price=Avg('books__price'))
    serializer_class = AuthorSerializer
    pagination_class = SomeCustomPagination


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().prefetch_related('line_items__book')
    serializer_class = OrderSerializer


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        # Check if countries are cached
        countries = cache.get("countries")
        if countries:
            print("Countries are cached")
            return Response(countries)

        response = super().list(request, *args, **kwargs)

        cache.set("countries", response.data)

        return response
