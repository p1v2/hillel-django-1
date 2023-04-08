from datetime import datetime

from django.core.management import BaseCommand
from django.db.models import Avg, F, Q, Count, Sum, Min

from students.models import Students, LessonStudent, Lessons, Teachers


class Command(BaseCommand):
    def handle(self, *args, **options):
        #  1. Усі студенти чає прізвище починається з літери "S"
        # query = Students.objects.using('students').filter(last_name__startswith="S")
        # students = [(student.first_name, student.last_name) for student in query]
        # print(students)

        # 2. Усі студенти які отримали оцінку 8 або більше за певну дату (виберіть таку дату щоб знайшовся хоча б один студент)
        # query = LessonStudent.objects.using('students').select_related('student').select_related('lesson')\
        #     .filter(mark__gte=8)\
        #     .filter(lesson__date_time__year='2022', lesson__date_time__month='04', lesson__date_time__day='28')
        # query = [(q.student.first_name, q.student.last_name, q.mark, q.lesson.date_time) for q in query]
        # print(query)

        #  3. Усі уроки, які викладає викладач з прізвищем "Rogers"
        # query = Lessons.objects.using('students').select_related('teacher').filter(teacher__last_name='Rogers')
        # query = [(q.teacher.first_name, q.teacher.last_name, q.topic, q.date_time) for q in query]
        # print(query)

        #  4. Усіх студентів, чия середня оцінка вище ніж середня оцінка класу для певного уроку
        # select particular lesson on the specified date
        # lesson = Lessons.objects.using('students').get(date_time__year='2022', date_time__month='04', date_time__day='28')
        # # calculate the average mark of class for the lesson
        # average_mark = LessonStudent.objects.using('students').filter(lesson=lesson).aggregate(Avg('mark'))['mark__avg']
        # # students whose average mark is higher than the average mark for the class on the specified date
        # students = Students.objects.using('students').annotate(avg_mark=Avg('lessonstudent__mark'))\
        #     .filter(Q(lessonstudent__lesson=lesson) & Q(avg_mark__gt=average_mark)).order_by('-avg_mark')
        # for student in students:
        #     print(student.first_name, student.last_name, student.avg_mark)

        #  5. Топ-5 студентів із найвищою оцінкою за всі уроки
        # query = LessonStudent.objects.using('students')\
        #     .values('student__id', 'student__first_name', 'student__last_name').annotate(sum_mark=Sum('mark'))\
        #     .order_by('-sum_mark')[:5]
        # print(query)

        #  6. Відсоток студентів, які отримали оцінку 5 або вище для кожного уроку
        # best_students = 100 * (Students.objects.using('students').count() - Students.objects.using('students')
        #             .annotate(min_mark=Min('lessonstudent__mark')).count()) / Students.objects.using('students').count()
        # print(best_students)

        #  7. Кількість уроків, які провів кожен викладач
        # query = Teachers.objects.using('students').annotate(amount_of_lessons=Count('lessons__id'))
        # for teacher in query:
        #     print(teacher.first_name, teacher.last_name, teacher.amount_of_lessons)

        #  8. Всі уроки, які провів викладач з прізвищем "Rogers"
        #     обʼєднані з уроками які провів викладач з прізвищем "Huerta"
        query = Teachers.objects.using('students').annotate(amount_of_lessons=Count('lessons__id'))\
            .filter(last_name='Rogers').union(Teachers.objects.using('students')
            .annotate(amount_of_lessons=Count('lessons__id')).filter(last_name='Huerta'))
        for teacher in query:
            print(teacher.first_name, teacher.last_name, teacher.amount_of_lessons)