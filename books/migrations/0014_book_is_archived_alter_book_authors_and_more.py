# Generated by Django 4.1.6 on 2023-03-06 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_book_count_selled'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_archived',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(blank=True, to='books.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.country'),
        ),
    ]
