from django.contrib.auth.models import User
from django.db import models

from books.models import Author
from books.models import Country
from books.models.item import Item
from books.models.mixins import CheapMixin


class BookQueryset(models.QuerySet, CheapMixin):
    def starred(self):
        return self.filter(authors__starred=True)

    def sold(self):
        return self.filter(count_sold__gt=0)

    def select_related(self, *fields):
        return super().select_related("country", *fields)

    def with_country(self):
        return self.filter(country__isnull=False)

    def with_country_name(self):
        return self.select_related("country").annotate(country_name=models.F("country__name"))


class BookManager(models.Manager):
    _queryset_class = BookQueryset
    def get_queryset(self):
        return super().get_queryset().prefetch_related("authors").filter(is_archived=False)

    def create(self, **kwargs):
        kwargs["is_archived"] = False
        return super().create(**kwargs)

    def update(self, **kwargs):
        kwargs["is_archived"] = False
        return super().update(**kwargs)

    def starred(self):
        return self.get_queryset().starred()


class ArchivedBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=True)


class Book(Item):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True, db_index=True)
    authors = models.ManyToManyField(Author)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_archived = models.BooleanField(default=False)
    code = models.IntegerField(blank=True, null=True, unique=True)

    objects = BookManager()
    archived_objects = ArchivedBookManager()

    @property
    def authors_string(self):
        authors_names = []

        for author in self.authors.all():
            authors_names.append(f"{author.first_name} {author.last_name}")

        return ", ".join(authors_names)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "books"
        ordering = ["-price", "count_sold"]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        index_together = [("country", "name")]
        default_related_name = "books"

        # Do not run migrations for this model
        managed = False
