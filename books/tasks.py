import os

from celery import shared_task
from django.core.mail import EmailMessage

from books.models import Order
from books.telegram import send_telegram_message
from books.models.author import Author


# @shared_task(autoretry_for=(BaseException,), retry_backoff=2)
# def on_order_save(order_id):
#     your_name = "Василь Сіромаха"
#     author = Author.objects.get(id=order_id)
#     # author = Order.objects.get(id=order_id)
#
#     text = f"Hi, {author.first_name}! You have a your book sold. Sincerely, your {your_name}"
#
#     print("Sending telegram message...2")
#     send_telegram_message(text)

    # send_customer_email.delay(instance.id)


@shared_task
def send_customer_email(order_id):
    order = Order.objects.get(id=order_id)

    mail = EmailMessage("Order created", "", os.environ["GMAIL_FROM_EMAIL"], [order.customer.email])

    mail.attach("order.txt", f"Order {order.id} created", "text/plain")
    mail.send()


@shared_task
def run_every_5_seconds():
    print("The task is running every 5 seconds...")

