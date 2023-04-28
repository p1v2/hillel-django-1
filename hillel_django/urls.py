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
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view

from rest_framework import routers, permissions

from books.auth_views import login_view, register_view, logout_view
from books.views import books_csv_export, books_pdf_export
from books.viewsets import BookViewSet, AuthorViewSet, OrderViewSet, CountryViewSet, AuthorBooksViewSet
from hillel_django.views import now_page

schema_view = get_schema_view(
   openapi.Info(
      title="Books API API",
      default_version='v1',
      contact=openapi.Contact(email="vitalii@vitalii.tech"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)
router.register("orders", OrderViewSet)
router.register("countries", CountryViewSet)
router.register("authors/(?P<author_id>\\d+)/books", AuthorBooksViewSet, basename="author-books")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("graphql", GraphQLView.as_view(graphiql=True)),
    # path('api/token-auth', obtain_auth_token),
    # path('api/session-auth', session_auth),
    path("api/login", login_view),
    path("api/register", register_view),
    path("api/logout", logout_view),
    path('cached-page', cache_page(5)(now_page)),
    path('non-cached-page', now_page),
    path('books-csv', books_csv_export),
    path('books-pdf', books_pdf_export),
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("accounts/", include("allauth.urls")),
    path("", TemplateView.as_view(template_name="index.html")),
    path("logout", LogoutView.as_view()),
]
