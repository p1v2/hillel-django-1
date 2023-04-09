from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Country(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=False, null=True, help_text="Description of the country")

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


@receiver(post_save, sender=Country)
@receiver(post_delete, sender=Country)
def reset_countries_cache(*args, **kwargs):
    print("Resetting countries cache")
    prepopulate_countries_cache()


def prepopulate_countries_cache():
    from django.core.cache import cache

    # Very long function
    countries = Country.objects.all()

    from books.serializers import CountrySerializer
    serializer = CountrySerializer(countries, many=True)
    cache.delete("countries")
    cache.set("countries", serializer.data)
    print("Prepopulated countries cache")
