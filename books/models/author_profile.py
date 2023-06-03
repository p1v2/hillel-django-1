from django.db import models
from books.models.country import Country


class AuthorProfile(models.Model):
    bio = models.TextField()
    birth_date = models.DateField()
    death_date = models.DateField(null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


