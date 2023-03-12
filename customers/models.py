from django.db import models


class Customer(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
