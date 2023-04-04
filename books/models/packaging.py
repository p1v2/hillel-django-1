from django.db import models


class Packaging(models.Model):
    length = models.FloatField()


class GiftPackaging(Packaging):
    gift_message = models.TextField()
