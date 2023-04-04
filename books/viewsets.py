from django.core.cache import cache
from django.db.models import Count, Avg
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from books.models import Book, Author, Order
from books.pagination import BookPagination, SomeCustomPagination
from books.serializers import BookSerializer, AuthorSerializer, OrderSerializer
from hillel_django.permissions import IsSellerOrAdminOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('country').prefetch_related('authors').filter(is_archived=False)

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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # Reset books cache
        keys = cache.keys('books:*')
        for key in keys:
            cache.delete(key)

        return response


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().annotate(books_count=Count('books'), average_price=Avg('books__price'))
    serializer_class = AuthorSerializer
    pagination_class = SomeCustomPagination


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().prefetch_related('line_items__book')
    serializer_class = OrderSerializer
