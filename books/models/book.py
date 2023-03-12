from django.contrib.auth.models import User
from django.db import models

from books.models import Author
from books.models import Country


class Book(models.Model):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    price = models.FloatField()
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    count_sold = models.IntegerField(default=0)

    @property
    def authors_string(self):
        authors_names = []

        for author in self.authors.all():
            authors_names.append(f"{author.first_name} {author.last_name}")

        return ", ".join(authors_names)

    def __str__(self):
        return f"{self.name} {self.authors} {self.pages_count} {self.country} {self.seller} {self.price}"

    def get_information(self):
        return f"Name: {self.name}\nCount of pages: {self.pages_count}\nCountry: {self.country}\nPrice: {self.price}"
