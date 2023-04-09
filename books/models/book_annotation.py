from django.db import models


class BookAnnotation(models.Model):
    book_id = models.IntegerField()
    description = models.TextField()

    class Meta:
        managed = False
