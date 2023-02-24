import random

from django.core.management import BaseCommand

from books.models import Country, Book


class Command(BaseCommand):
    def handle(self, *args, **options):
        for book in Book.objects.all():
            array = [True, False]
            is_archived = random.choice(array)
            book.is_archived = is_archived
            book.save()
