from django.db.models import Q
from django_filters import FilterSet, CharFilter, NumberFilter, BooleanFilter, ModelMultipleChoiceFilter
from django_filters.fields import Lookup

from books.models import Book


class BookFilter(FilterSet):
    # In SQL: SELECT * FROM books WHERE name LIKE '%some name%'
    # icontains - case insensitive contains
    # Book.objects.filter(name__icontains="some name")
    # name = CharFilter(field_name="name", lookup_expr="icontains")

    name_starts = CharFilter(field_name="name", lookup_expr="startswith")

    # contains - case sensitive contains
    # startswith - case sensitive startswith

    count_sold_gte = NumberFilter(field_name="count_sold", lookup_expr="gte")

    # exclude means: Books.objects.exclude(seller__isnull=True)
    # which is opposite to Books.objects.filter(seller__isnull=True)
    has_seller = BooleanFilter(field_name="seller", lookup_expr="isnull", exclude=True)

    author_first_name = CharFilter(field_name="authors__first_name", lookup_expr="icontains")
    country = CharFilter(field_name="country__name", lookup_expr="icontains")

    author_id = NumberFilter(field_name="authors__id", lookup_expr="exact")

    country_id = NumberFilter(field_name="country__id", lookup_expr="exact")

    q = CharFilter(method="filter_query")

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(authors__first_name__icontains=value) |
            Q(country__name__icontains=value)
        )


    class Meta:
        model = Book
        fields = ["name", "name_starts", "count_sold_gte", "has_seller", "author_first_name"]
