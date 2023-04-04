from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


class BookPagination(CursorPagination):
    ordering = 'id'
    page_size = 100


class SomeCustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'some_custom_page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'api_type': 'paginated'
        }, headers={"X-Total-Count": self.page.paginator.count})
