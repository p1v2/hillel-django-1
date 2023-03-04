from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from books.telegram import send_telegram_message
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


@receiver(post_save, sender=Order)
def on_order_save(sender, instance: Order, created, **kwargs):

    text = f"ORDER {instance.id} CREATED.\nPhone: {instance.customer.phone_number}"
    if created:
        send_telegram_message(text)
