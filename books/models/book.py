from django.contrib.auth.models import User
from django.db import models

from books.models import Author
from books.models import Country


class Book(models.Model):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE,blank=True)
    price = models.FloatField()
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    count_sold = models.IntegerField(default=0)
    is_archived = models.BooleanField(null=True)

    @property
    def authors_string(self):
        authors_names = []

        for author in self.authors.all():
            authors_names.append(f"{author.first_name} {author.last_name}")

        return ", ".join(authors_names)

    def __str__(self):
        return self.name
