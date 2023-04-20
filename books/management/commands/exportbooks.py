from django.core.management import BaseCommand
from django.contrib.auth.models import User

from books.models import Book, Author
from google_sheets import write_to_google_sheets


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Book.objects.all()[:100]
        authors = Author.objects.all()

        user = User.objects.get(username="vitaliipavliuk")

        write_to_google_sheets(user, books, authors)
