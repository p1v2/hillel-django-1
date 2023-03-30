import random

from django.core.management import BaseCommand

from faker import Faker

from students.models import Teachers

fake = Faker(locale="uk")


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(50):
            first_name = fake.first_name()
            last_name = fake.last_name()
            subject = random.choice(("Математика", "Філологія", "Кібербезпека", "Програмування"))
            Teachers.objects.create(first_name=first_name, last_name=last_name, subject=subject)
