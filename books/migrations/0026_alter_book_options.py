# Generated by Django 4.1.6 on 2023-03-23 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0025_pen_alter_book_index_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'default_related_name': 'books', 'managed': False, 'ordering': ['-price', 'count_sold'], 'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
    ]
