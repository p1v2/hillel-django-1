from rest_framework.permissions import BasePermission

SAFE_HTTP_METHODS = ["GET", "HEAD"]


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True
        if request.method in SAFE_HTTP_METHODS:
            return True

        return False


class IsSellerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.user == obj.seller:
            return True

        if request.method in SAFE_HTTP_METHODS:
            return True

        return False
