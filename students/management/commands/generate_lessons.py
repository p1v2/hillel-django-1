import random
from datetime import datetime

from django.core.management import BaseCommand

from faker import Faker

from students.models import Lessons, Teachers

fake = Faker(locale="uk")


class Command(BaseCommand):
    def handle(self, *args, **options):
        temp = ["Математика", "Філологія", "Кібербезпека", "Програмування"]
        for i in range(4):
            topic = temp[i]
            date_time = datetime.now()
            teacher = Teachers.objects.only("id")[i]
            Lessons.objects.create(topic=topic, date_time=date_time, teacher=teacher)

