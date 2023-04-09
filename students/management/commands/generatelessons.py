from datetime import datetime
from django.core.management import BaseCommand
from students.models import Lessons, Teachers


class Command(BaseCommand):
    def handle(self, *args, **options):
        item = ["Українська", "Право", "Програмування", "Історія"]
        for i in range(4):
            topic = item[i]
            date_time = datetime.now()
            teacher = Teachers.objects.only("id")[i]
            Lessons.objects.create(topic=topic, date_time=date_time, teacher=teacher)