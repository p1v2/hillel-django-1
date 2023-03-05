from django.db import models
from rest_framework.authtoken.admin import User


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    price = models.FloatField()
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_archived = models.BooleanField(null=True, default=False)
    count_selled = models.IntegerField(null=True)
    is_archived = models.BooleanField(null=True, default=False)

    def get_information(self):
        info_author = {
            'first_name': Author.first_name,
            'last_name': Author.last_name,
        }

        info_book = {
            'name': self.name,
            'authors': self.authors,
            'pages_count': self.pages_count,
            'country': self.country,
            'seller': self.seller,
            'info_authors': info_author,
        }

        return info_book

    def __str__(self):
        return self.name
