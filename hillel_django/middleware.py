from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Pre Django 1.10
# class CustomLoggingMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         print('request', request)
#         ip = get_client_ip(request)
#         if ip == "127.0.0.1":
#             return HttpResponseForbidden("Please, use another IP")
#         return None
#
#     def process_response(self, request, response):
#         print('response', response)
#         return response


class CustomLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('request', request)
        ip = get_client_ip(request)
        if ip == "127.0.0.1":
            response = HttpResponseForbidden("You are not allowed to access this page")
        else:
            response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print('response', response)

        return response
