from django.core.management import BaseCommand
from faker import Faker
from students.models import Students


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(100):
            first_name = Faker.first_name()
            last_name = Faker.last_name()
            Students.objects.create(first_name=first_name, last_name=last_name)