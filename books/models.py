from django.db import models


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
    count_selled = models.IntegerField(null=True)

    def __str__(self):
        return self.name
