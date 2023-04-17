from django.core.management import BaseCommand

from books.models import Book, Author
from google_sheets import write_to_google_sheets


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Book.objects.all()[:100]
        authors = Author.objects.all()

        write_to_google_sheets(books, authors)
