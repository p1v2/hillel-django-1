from django.core.cache import cache
from django.db.models import Count, Avg
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from books.filters import BookFilter
from books.models import Book, Author, Order, Country
from books.pagination import BookPagination, SomeCustomPagination
from books.serializers import BookSerializer, AuthorSerializer, OrderSerializer, CountrySerializer, \
    AuthorBooksSerializer
from hillel_django.permissions import IsSellerOrAdminOrReadOnly


class BaseBookViewset(ModelViewSet):

    serializer_class = BookSerializer
    permission_classes = [IsSellerOrAdminOrReadOnly]
    authentication_classes = [SessionAuthentication]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # ordering_fields = ["name", "price"]
    filterset_class = BookFilter


class BookViewSet(BaseBookViewset):
    queryset = Book.objects.select_related('country').prefetch_related('authors')

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

    def destroy(self, request, *args, **kwargs):
        print(f"Destroying book {kwargs}")
        return super().destroy(request, *args, **kwargs)


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


class AuthorBooksViewSet(BaseBookViewset):
    serializer_class = AuthorBooksSerializer


    def create(self, request, *args, **kwargs):
        request.data['authors'] = [self.kwargs['author_id']]

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return Book.objects.filter(authors__id=self.kwargs['author_id'])

    def list(self, request, *args, **kwargs):
        # Get is_archived from GET params
        is_archived = request.GET.get('is_archived', False)

        # Get books according to is_archived
        if is_archived:
            self.queryset = self.queryset.filter(is_archived=True)

        return super().list(request, *args, **kwargs)
