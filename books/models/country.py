from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=False, null=True, help_text="Description of the country")

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
