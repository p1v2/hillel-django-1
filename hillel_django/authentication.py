from urllib.request import Request

import rest_framework
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import WrappedAttributeError


class GloryToUkraineAuthentication(BaseAuthentication):
    def authenticate(self, request):
        query_params = request.GET

        if query_params.get("haslo") == "SlavaUkraini":
            return User.objects.get(username="admin"), None


class SecretHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        secret_header = request.META.get("HTTP_SECRET_HEADER")
        if not secret_header:
            raise AuthenticationFailed()
        try:
            if secret_header.startswith("Some super secret"):
                username = secret_header.split(" ")[-1]
                return User.objects.get(username=username), None
        except User.DoesNotExist:
            raise AuthenticationFailed()


