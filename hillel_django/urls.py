"""hillel_django URL Configuration

The `urlpatterns` list routes URLs to views.py. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views.py
    1. Add an import:  from my_app import views.py
    2. Add a URL to urlpatterns:  path('', views.py.home, name='home')
Class-based views.py
    1. Add an import:  from other_app.views.py import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from books.views import books_csv_export, books_pdf_export
from books.viewsets import BookViewSet, AuthorViewSet, OrderViewSet, CountryViewSet
from hillel_django.views import session_auth, now_page

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)
router.register("orders", OrderViewSet)
router.register("countries", CountryViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token-auth', obtain_auth_token),
    path('api/session-auth', session_auth),
    path('cached-page', cache_page(5)(now_page)),
    path('non-cached-page', now_page),
    path('books-csv', books_csv_export),
    path('books-pdf', books_pdf_export)
]
