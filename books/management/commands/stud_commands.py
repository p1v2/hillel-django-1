from django.core.management import BaseCommand
from students.models import Students, Lessons, Teachers, LessonStudent
from django.db.models import Count
from django.db.models import Avg, Max, Q

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Усі студенти чає прізвище починається з літери "S"
        students = Students.objects.filter(last_name__startswith='S')
        for student in students:
            print(student.first_name, student.last_name)

        # Усі студенти які отримали оцінку 8 або більше за певну дату.

        lesson_students = LessonStudent.objects.filter(mark__gte=8, lesson__date_time__date='2022-11-21')
        for lesson_student in lesson_students:
            print(lesson_student.student.first_name, lesson_student.student.last_name, lesson_student.mark,
                  lesson_student.lesson.date_time)

        # Усі уроки, які викладає викладач з прізвищем "Rogers"
        lessons = Lessons.objects.filter(teacher__last_name='Rogers')
        for lesson in lessons:
            print(lesson.topic)

        # Усіх студентів, чия середня оцінка вище ніж середня оцінка класу для певного уроку

        lesson_id = 2
        average_class_mark = (
            LessonStudent.objects
            .filter(lesson_id=lesson_id)
            .aggregate(avg_mark=Avg('mark'))['avg_mark']
        )

        students_with_higher_avg = (
            LessonStudent.objects
            .values('student')
            .annotate(avg_mark=Avg('mark'))
            .filter(avg_mark__gt=average_class_mark)
            .order_by('-avg_mark')
        )

        student_ids = students_with_higher_avg.values_list('student', flat=True)
        students = Students.objects.filter(id__in=student_ids).values_list('first_name', 'last_name')
        for first_name, last_name in students:
            print(first_name, last_name)

        # Топ-5 студентів із найвищою оцінкою за всі уроки.

        top_5_students = (
            LessonStudent.objects
            .values('student')
            .annotate(avg_mark=Avg('mark'), max_mark=Max('mark'))
            .filter(avg_mark__isnull=False)
            .order_by('-max_mark', '-avg_mark')[:5]
        )
        student_ids = top_5_students.values_list('student', flat=True)
        students = Students.objects.filter(id__in=student_ids).values_list('first_name', 'last_name')
        for first_name, last_name in students:
            print(first_name, last_name)

        # Відсоток студентів, які отримали оцінку 5 або вище для кожного уроку.
        queryset = (
            LessonStudent.objects
            .values('lesson_id')
            .annotate(
                num_students=Count('id'),
                num_passing_students=Count('id', filter=Q(mark__gte=5)),
                percent_passing_students=100 * Count('id', filter=Q(mark__gte=5)) / Count('id'),
            )
            .order_by('lesson_id')
            .values('lesson_id', 'percent_passing_students')
        )

        for row in queryset:
            print(f"Урок {row['lesson_id']}: {row['percent_passing_students']}% студентів отримали оцінку 5 або вище.")

        # # Кількість уроків, які провів кожен викладач.
        teachers =Teachers.objects.annotate(lesson_count=Count('lessons')).values('first_name', 'last_name', 'lesson_count')
        for teacher in teachers:
            print(f"{teacher['first_name']} {teacher['last_name']}: {teacher['lesson_count']} lessons")

        # # Всі уроки, які провів викладач з прізвищем "Rogers" обʼєднані з уроками які провів викладач з прізвищем "Huerta".
        lessons = Lessons.objects.filter(teacher__last_name__in=['Rogers', 'Huerta'])
        for lesson in lessons:
            print(
                f"Lesson topic: {lesson.topic}, Teacher: {lesson.teacher.first_name} {lesson.teacher.last_name}")

