from django.core.management import BaseCommand
from django.db.models import Q, F, Aggregate, Avg, Max, Count, Sum
from students.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        #  Усі студенти чає прізвище починається з літери "S"
        # queryset = Students.objects.filter(first_name__startswith="С")

        #  Усі студенти які отримали оцінку 8 або більше за певну дату (виберіть таку дату щоб знайшовся хоча б один студент).
        #  queryset = LessonStudent.objects.filter(mark__gte=8, lesson__date_time__startswith='2023-03-28')
        
        #  Усі уроки, які викладає викладач з прізвищем "Ковалюк"
        #  queryset = Teachers.objects.filter(last_name="Ковалюк")
        
        #  Усіх(filter) студентів, чия (avg)середня оцінка вище ніж (avg)середня оцінка класу для певного уроку(group by)
        #  queryset = LessonStudent.objects.filter(mark__gte=Avg('mark')).annotate(Avg("mark")).values('student__first_name')
        

        #  Топ-5 студентів із найвищою оцінкою за всі уроки.
        #  queryset = LessonStudent.objects.all().annotate(Avg("mark")).values('student__first_name').order_by("mark")[:5]
        
        #  Відсоток студентів, які отримали оцінку 5 або вище для кожного уроку.
        #queryset = LessonStudent.objects.annotate(result=Count("mark", filter=Q(mark__gte=5)))
        #counter = 0
        #for i in queryset:
        #   temp = None
        #    if i.result != 0:
        #        counter += 1
        #        temp = (i.result / counter) * 100
        #    print(temp)

        #  Кількість уроків, які провів кожен викладач.
        #  queryset = Lessons.objects.values("teacher_id").annotate(Count("topic"))
        
        #  Всі уроки, які провів викладач з прізвищем "Rogers" обʼєднані з уроками які провів викладач з прізвищем "Huerta".
        #  queryset = Lessons.objects.filter(teacher="Rogers").union(Lessons.objects.filter(teacher="Huerta"))
        