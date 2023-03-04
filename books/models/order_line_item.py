from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Book
from books.models.order import Order
from books.telegram import send_telegram_message


class OrderLineItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="line_items")
    quantity = models.IntegerField()


@receiver(post_save, sender=OrderLineItem)
def on_order_save(sender, instance: OrderLineItem, created, **kwargs):

    if created:
        send_telegram_message(f"{instance.book.name} - {instance.quantity}")
