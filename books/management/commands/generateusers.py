from django.core.management import BaseCommand
from faker import Faker
from rest_framework.authtoken.admin import User

from books.models import Book


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()

        for _ in range(10):
            user = User.objects.create(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            user.set_password("gddgdd")
            user.save()

        for book in Book.objects.all():
            book.seller = User.objects.order_by('?').first()
            book.save()
