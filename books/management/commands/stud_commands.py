from django.core.management import BaseCommand
from students.models import Students, Lessons, Teachers, LessonStudent
from django.db.models import Count
from django.db.models import Avg, Max


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Усі студенти чає прізвище починається з літери "S"
        students = Students.objects.filter(last_name__startswith='S')
        for student in students:
            print(student.first_name, student.last_name)

        # Усі студенти які отримали оцінку 8 або більше за певну дату.

        lesson_students = LessonStudent.objects.filter(mark__gte=8, lesson__date_time__startswith='2022-11-21')
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

        students = Students.objects.filter(id__in=[s['student'] for s in students_with_higher_avg])
        for student in students:
            print(student.first_name, student.last_name)

        # Топ-5 студентів із найвищою оцінкою за всі уроки.

        top_5_students = (
            LessonStudent.objects
            .values('student')
            .annotate(avg_mark=Avg('mark'), max_mark=Max('mark'))
            .filter(avg_mark__isnull=False)
            .order_by('-max_mark', '-avg_mark')[:5]
        )
        students = Students.objects.filter(id__in=[s['student'] for s in top_5_students])
        for student in students:
            print(student.first_name, student.last_name)

        # Відсоток студентів, які отримали оцінку 5 або вище для кожного уроку.

        lessons = LessonStudent.objects.values('lesson_id').distinct()

        for lesson in lessons:
            lesson_id = lesson['lesson_id']
            students_count = LessonStudent.objects.filter(lesson_id=lesson_id).count()
            top_students_count = LessonStudent.objects.filter(lesson_id=lesson_id, mark__gte=5).count()
            if students_count > 0:
                top_students_percentage = (top_students_count / students_count) * 100
            else:
                top_students_percentage = 0
            print(f"Lesson {lesson_id}: {top_students_percentage:.2f}% students got 5 or higher")

        # Кількість уроків, які провів кожен викладач.
        teachers =Teachers.objects.annotate(lesson_count=Count('lessons')).values('first_name', 'last_name', 'lesson_count')
        for teacher in teachers:
            print(f"{teacher['first_name']} {teacher['last_name']}: {teacher['lesson_count']} lessons")

        # Всі уроки, які провів викладач з прізвищем "Rogers" обʼєднані з уроками які провів викладач з прізвищем "Huerta".
        lessons = Lessons.objects.filter(teacher__last_name__in=['Rogers', 'Huerta'])
        for lesson in lessons:
            print(
                f"Lesson topic: {lesson.topic}, Teacher: {lesson.teacher.first_name} {lesson.teacher.last_name}")
            
            
