# Generated by Django 4.1.7 on 2023-02-15 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_book_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='count_selled',
            field=models.IntegerField(null=True),
        ),
    ]
