from time import sleep

from celery import shared_task
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from books.telegram import send_telegram_message
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


@receiver(post_save, sender=Order)
def on_order_save_in_thread(sender, instance: Order, created, **kwargs):
    if created:
        on_order_save.delay(instance.id)


@shared_task(autoretry_for=(BaseException,), retry_backoff=2)
def on_order_save(order_id):
    your_name = "Василь Сіромаха"
    order = Order.objects.get(id=order_id)
    book = order.line_items.first().book
    authors = book.authors.filter(telegram_account_id__isnull=False)
    for author in authors:
        telegram_account_id = author.telegram_account_id
        text = f"Hi, {author.first_name}! Your book has been sold. Sincerely, {your_name}"
        print(f"Sending telegram message to {author.first_name} {author.last_name}...")
        send_telegram_message(text, telegram_account_id)
    if not authors:
        print("No authors with telegram account found for this book.")

