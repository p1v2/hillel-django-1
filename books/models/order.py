from django.db import models

from books.models import Book
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    books = models.ManyToManyField(Book, through='OrderLineItem', related_name='orders')
