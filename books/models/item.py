from django.db import models


class Item(models.Model):
    price = models.FloatField()
    count_sold = models.IntegerField(default=0)

    class Meta:
        abstract = True
