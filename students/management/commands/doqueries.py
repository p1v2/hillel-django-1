from django.core.management import BaseCommand
from django.db.models import Q, F, Aggregate, Avg, Max, Count, Sum
from students.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1. Усі студенти чає прізвище починається з літери "S"
        # students = [(student.first_name, student.last_name) for student in Students.objects.using('students').filter(last_name__startswith="S"]
        # print(students)

        # 2. Усі студенти які отримали оцінку 8 або більше за певну дату (виберіть таку дату щоб знайшовся хоча б один студент).
        # greater_than_8 = LessonStudent.objects.filter(mark__gte=8, lesson__date_time__startswith='2023-04-28')
        # print(greater_than_8)

        # 3. Усі уроки, які викладає викладач з прізвищем "Rogers"
        # rogers = Lessons.objects.filter(teacher__last_name="Rogers")
        # print(rogers)

        # 4. Усіх студентів, чия середня оцінка вище ніж середня оцінка класу для певного уроку
        # greater_than_avg = Students.objects.filter(lessonstudent__mark__gte=Avg('lessonstudent__mark')).annotate(Avg("lessonstudent__mark")).values('first_name')
        # print(greater_than_avg)

        # 5. Топ-5 студентів із найвищою оцінкою за всі уроки.
        # top_5 = LessonStudent.objects.all().annotate(Avg("mark")).values('student__first_name').order_by("mark")[:5]
        # print(top_5)

        # 6. Відсоток студентів, які отримали оцінку 5 або вище для кожного уроку.
        # bright_minds = (Students.objects.using('students').count() - Students.objects.using('students').annotate(min_mark=Min('lessonstudent__mark')).count()) / Students.objects.using('students').count() * 100
        # print(bright_mind)

        # 7. Кількість уроків, які провів кожен викладач.
        # count_lessons = Lessons.objects.values("teacher_id").annotate(Count("topic"))
        # print(count_lessons)

        # 8. Всі уроки, які провів викладач з прізвищем "Rogers" обʼєднані з уроками які провів викладач з прізвищем "Huerta".
        # collaboration = Lessons.objects.filter(teacher="Rogers").union(Lessons.objects.filter(teacher="Huerta"))

