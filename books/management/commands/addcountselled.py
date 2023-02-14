from django.core.management import BaseCommand
from random import randint

from faker import Faker

from books.models import Book

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for book in Book.objects.all():
            random_value = randint(1000, 10000)

            book.count_selled = random_value
            book.save()
