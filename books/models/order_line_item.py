from django.db import models

from books.models import Book
from books.models.order import Order


class OrderLineItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="line_items")
    quantity = models.IntegerField()
