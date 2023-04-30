import os

from celery import shared_task
from django.db.models import Sum
from django.core.mail import EmailMessage

from books.models import Order, Author, Book, OrderLineItem
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


@shared_task(autoretry_for=(BaseException,), retry_backoff=2)
def order_created(order_id):
    instance = OrderLineItem.objects.get(id=order_id)
    book_name = instance.book.name
    b: Book = Book.objects.get(name=book_name)
    authors = b.authors.all()
    for author in authors:
        if author.telegram_account_id:
            text = f'"Hi, {author.first_name}! You have your book sold. Sincerely, your Greg Ponomarenko" '
            send_telegram_message(text, author.telegram_account_id)


@shared_task
def timetable_sending():
    authors = Author.objects.annotate(total_count_sold=Sum('book__count_sold'))
    for author in authors:
        if author.telegram_account_id:
            text = f'Hi, {author.first_name}! There is already {author.total_count_sold} of your books being sold"'
            send_telegram_message(text, author.telegram_account_id)
