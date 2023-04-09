from django.core.management import BaseCommand
from django.db.models import Q, F, Aggregate, Avg, Max, Count, Sum
from students.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
        #  Усі студенти з прізвищем на "S"
        # queryset = Students.objects.filter(first_name__startswith="S")

        #  Усі студенти які отримали оцінку 8 або більше за якусь дату.
        #  queryset = LessonStudent.objects.filter(mark__gte=8, lesson__date_time__startswith='2023-03-28')

        #  Усі уроки, які викладає викладач з прізвищем "Rogers"
        #  queryset = Lessons.objects.filter(teacher__last_name="Rogers")


        #  Усіх студентів, чия середня оцінка вище ніж середня оцінка класу для певного уроку.
        #  queryset = Students.objects.filter(lessonstudent__mark__gte=Avg('lessonstudent__mark')).annotate(Avg("lessonstudent__mark")).values('first_name')


        #  Топ-5 студентів із найвищою оцінкою за всі уроки.
        #  queryset = LessonStudent.objects.all().annotate(Avg("mark")).values('student__first_name').order_by("mark")[:5]

        #? Відсоток студентів, які отримали оцінку 5 або вище для кожного уроку.
        #  queryset = LessonStudent.objects.filter(mark__gte=5).values('lesson_id').annotate(num_students=Count('id'), num_passing_students=Count('id', filter=Q(mark__gte=5))).annotate(percent_passing_students=100 * Avg('num_passing_students') / Avg('num_students')).values('lesson_id', 'percent_passing_students')

        #  Кількість уроків, які провів кожен викладач.
        #  queryset = Lessons.objects.values("teacher_id").annotate(Count("topic"))

        #  Всі уроки, які провів викладач з прізвищем "Rogers" обʼєднані з уроками які провів викладач з прізвищем "Huerta".
        #  queryset = Lessons.objects.filter(teacher="Rogers").union(Lessons.objects.filter(teacher="Huerta"))

