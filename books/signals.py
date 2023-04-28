from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Order, OrderLineItem
from books.tasks import on_order_save, new_order_created


# @receiver(post_save, sender=Order)
# def on_order_save_in_thread(sender, instance: Order, created, **kwargs):
#     if created:
#         on_order_save.delay(instance.id)


@receiver(post_save, sender=OrderLineItem)
def new_order_created_signal(sender, instance: OrderLineItem, created, **kwargs):
    if created:
        # new_order_created.delay(instance.id)
        new_order_created.delay(instance.id)