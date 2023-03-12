import os

from celery import shared_task
from django.core.mail import EmailMessage

from books.models import Order
from books.telegram import send_telegram_message
from books.models.author import Author
from books.models import Book


# @shared_task(autoretry_for=(BaseException,), retry_backoff=2)
# def on_order_save(order_id):
#     instance = Order.objects.get(id=order_id)
#
#     text = f"""
# ORDER {instance.id} CREATED.
# Phone: {instance.customer.phone_number}
# """
#
#     for line_item in instance.line_items.all():
#         text += f"{line_item.book.name} - {line_item.quantity}\n"
#
#     print("Sending telegram message...")
#
#     send_telegram_message(text)
#
#     send_customer_email.delay(instance.id)
#
#
# @shared_task
# def send_customer_email(order_id):
#     order = Order.objects.get(id=order_id)
#
#     mail = EmailMessage("Order created", "", os.environ["GMAIL_FROM_EMAIL"], [order.customer.email])
#
#     mail.attach("order.txt", f"Order {order.id} created", "text/plain")
#     mail.send()


@shared_task
def run_every_5_seconds():
    print("The task is running every 5 seconds...")

@shared_task
def run_on_cron_schedule_count_of_books():
    authors = Author.objects.filter(book__isnull=False)
    for author in authors:
        count_sold = Book.objects.filter(authors=author).count()
        if author.telegram_account_id is not None:
            telegram_account_id = author.telegram_account_id
            text = f"Hi, {author.first_name}! There is already {count_sold} of your books being sold"
            print(f"Sending telegram message to {author.first_name} {author.last_name}...")
            send_telegram_message(text, telegram_account_id)

    print('run_on_cron_schedule')



