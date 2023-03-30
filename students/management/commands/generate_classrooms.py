import random

from django.core.management import BaseCommand

from faker import Faker

from students.models import Classrooms

fake = Faker(locale="uk")


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(50):
            room_number = i
            capacity = random.randint(15, 30)
            Classrooms.objects.create(room_number=room_number, capacity=capacity)

