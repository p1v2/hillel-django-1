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
    name = models.CharField('name', max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    price = models.FloatField()
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def get_information(self):
        name_info = self.author.get_information()
        pages_count_info = self.genre.get_information()
        authors_info = self.genre.get_information()
        country_info = self.genre.get_information()
        price_info = self.genre.get_information()
        seller_info = self.genre.get_information()

        book_info = {
            'name': name_info,
            'pages_count': pages_count_info,
            'authors': authors_info,
            'country': country_info,
            'price': price_info,
            'seller': seller_info,
        }
        return book_info



    def __str__(self):
        return self.name
