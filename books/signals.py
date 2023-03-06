from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Order
from books.tasks import on_order_save


@receiver(post_save, sender=Order)
def on_order_save_in_thread(sender, instance: Order, created, **kwargs):
    if created:
        on_order_save.delay(instance.id)
