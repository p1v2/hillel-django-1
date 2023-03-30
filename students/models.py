# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Books(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=40)
    pages_count = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey('BooksCountry', models.DO_NOTHING, blank=True, null=True)
    price = models.FloatField()
    seller = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    count_sold = models.IntegerField()
    is_archived = models.BooleanField()
    code = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class BooksAuthor(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    profile = models.OneToOneField('BooksAuthorprofile', models.DO_NOTHING, blank=True, null=True)
    starred = models.BooleanField()
    bio = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books_author'
        unique_together = (('first_name', 'last_name'),)


class BooksAuthorprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    bio = models.TextField()
    birth_date = models.DateField()
    death_date = models.DateField(blank=True, null=True)
    country = models.ForeignKey('BooksCountry', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_authorprofile'


class BooksAuthors(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    author = models.ForeignKey(BooksAuthor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_authors'
        unique_together = (('book', 'author'),)


class BooksCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books_country'


class BooksGiftpackaging(models.Model):
    packaging_ptr = models.OneToOneField('BooksPackaging', models.DO_NOTHING, primary_key=True)
    gift_message = models.TextField()

    class Meta:
        managed = False
        db_table = 'books_giftpackaging'


class BooksOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('CustomersCustomer', models.DO_NOTHING)
    packaging = models.OneToOneField('BooksPackaging', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'books_order'


class BooksOrderlineitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField()
    book = models.ForeignKey(Books, models.DO_NOTHING)
    order = models.ForeignKey(BooksOrder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_orderlineitem'


class BooksPackaging(models.Model):
    id = models.BigAutoField(primary_key=True)
    length = models.FloatField()

    class Meta:
        managed = False
        db_table = 'books_packaging'


class BooksPen(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.FloatField()
    count_sold = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'books_pen'


class Classrooms(models.Model):
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'classrooms'


class CustomersCustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=254)
    phone_number = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'customers_customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryBeatClockedschedule(models.Model):
    clocked_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'


class DjangoCeleryBeatCrontabschedule(models.Model):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'


class DjangoCeleryBeatIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'


class DjangoCeleryBeatPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, blank=True, null=True)
    one_off = models.BooleanField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.DO_NOTHING, blank=True, null=True)
    expire_seconds = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'


class DjangoCeleryBeatPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'


class DjangoCeleryBeatSolarschedule(models.Model):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LessonClassroom(models.Model):
    lesson = models.ForeignKey('Lessons', models.DO_NOTHING)
    classroom = models.ForeignKey(Classrooms, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lesson_classroom'


class LessonStudent(models.Model):
    lesson = models.ForeignKey('Lessons', models.DO_NOTHING)
    student = models.ForeignKey('Students', models.DO_NOTHING)
    mark = models.IntegerField(blank=True, null=True)
    present = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lesson_student'


class Lessons(models.Model):
    topic = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    teacher = models.ForeignKey('Teachers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lessons'


class Students(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'students'


class Teachers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'teachers'
