from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication


class GloryToUkraineAuthentication(BaseAuthentication):
    def authenticate(self, request):
        secret_header = request.headers.get("secret")
        if secret_header:
            if secret_header.startswith("Some super secret "):
                username = secret_header.replace("Some super secret ", "")
                if username in self.users:
                    return True, username
        return False, None
