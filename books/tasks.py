import os

from celery import shared_task
from django.core.mail import EmailMessage

from books.models import Order
from books.telegram import send_telegram_message


@shared_task(autoretry_for=(BaseException,), retry_backoff=2)
def on_order_save(order_id):
    # if random() < 1:
    #     print("The task will be retried in some time...")
    #     raise ValueError("Some error occurred")

    instance = Order.objects.get(id=order_id)

    text = f"""
ORDER {instance.id} CREATED.
Phone: {instance.customer.phone_number}
"""

    for line_item in instance.line_items.all():
        text += f"{line_item.book.name} - {line_item.quantity}\n"

    print("Sending telegram message...")
    send_telegram_message(text)

    send_customer_email.delay(instance.id)


@shared_task
def send_customer_email(order_id):
    order = Order.objects.get(id=order_id)

    mail = EmailMessage("Order created", "", os.environ["GMAIL_FROM_EMAIL"], [order.customer.email])

    mail.attach("order.txt", f"Order {order.id} created", "text/plain")
    mail.send()
