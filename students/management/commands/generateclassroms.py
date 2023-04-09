import random
from django.core.management import BaseCommand
from students.models import Classrooms


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(40):
            room_number = i
            quantity = random.randint(10, 50)
            Classrooms.objects.create(room_number=room_number, quantity=quantity)