from django.db import models

from books.models import Book
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    packaging = models.OneToOneField('Packaging', null=True, on_delete=models.SET_NULL)
    # on_delete=models.CASCADE - if packaging is deleted, delete the order
    # on_delete=models.SET_NULL - if packaging is deleted, set the packaging to null
    # on_delete=models.PROTECT - if packaging is deleted, raise an error

    books = models.ManyToManyField(Book, through='OrderLineItem', related_name='orders')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
