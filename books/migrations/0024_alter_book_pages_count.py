# Generated by Django 4.1.6 on 2023-03-23 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0023_book_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pages_count',
            field=models.IntegerField(db_index=True, null=True),
        ),
    ]