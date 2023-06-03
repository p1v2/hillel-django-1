import graphene
from graphene_django import DjangoObjectType

from books.models import Book, Author, Country


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = ("name",)


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name")


class BookType(DjangoObjectType):
    country = graphene.Field(CountryType)
    authors = graphene.List(AuthorType)
    authors_string = graphene.String()

    def resolve_authors_string(self, info):
        authors_names = []

        for author in self.authors.all():
            authors_names.append(f"{author.first_name} {author.last_name}")

        return ", ".join(authors_names)

    def resolve_authors(self, info):
        return self.authors.all()

    class Meta:
        model = Book
        fields = ("id", "name", "price", "country", "authors")
