import os

from django.conf import settings
from rest_framework.authtoken.admin import User

from telegram import Bot

from celery import shared_task

from celery import shared_task
from django.core.mail import EmailMessage

from books.models import Order, Author
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


@shared_task
def run_every_5_seconds():
    print("The task is running every 5 seconds...")


@shared_task
def send_order_notification(order_id):
    order = Order.objects.get(id=order_id)
    author = order.book.author
    telegram_account_id = author.telegram_account_id

    if telegram_account_id:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        message = f"Hi, {author.first_name}! You have sold a book. Sincerely, your {settings.YOUR_NAME}"
        bot.send_message(chat_id=telegram_account_id, text=message)


@shared_task
def send_daily_sales_notification():
    authors = Author.objects.filter(telegram_account_id__isnull=False)

    for author in authors:
        count_of_books = Order.objects.filter(book__author=author).count()

        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        message = f"Hi, {author.first_name}! There is already {count_of_books} of your books being sold"
        bot.send_message(chat_id=author.telegram_account_id, text=message)
