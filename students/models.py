from django.db import models


class Classrooms(models.Model):
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'classrooms'


class LessonClassroom(models.Model):
    lesson = models.ForeignKey('Lessons', models.DO_NOTHING)
    classroom = models.ForeignKey('Classrooms', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'lesson_classroom'


class LessonStudent(models.Model):
    lesson = models.ForeignKey('Lessons', models.DO_NOTHING)
    student = models.ForeignKey('Students', models.DO_NOTHING)
    mark = models.IntegerField(blank=True, null=True)
    present = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lesson_student'


class Lessons(models.Model):
    topic = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    teacher = models.ForeignKey('Teachers', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'lessons'


class Students(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'students'


class Teachers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'teachers'


