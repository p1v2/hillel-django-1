from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from books.models.author_profile import AuthorProfile


class AuthorQueryset(models.QuerySet):
    def all(self):
        # Caching all authors
        cached = cache.get("authors")
        if cached:
            print("Authors from cache")
            return cached

        print("Authors from db")
        authors = Author.objects.all().prefetch_related("books")
        cache.set("authors", authors)
        return authors


class AuthorManager(models.Manager):
    _queryset_class = AuthorQueryset


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    telegram_account_id = models.IntegerField(null=True)
    bio = models.TextField(blank=True, null=True)
    profile = models.OneToOneField(AuthorProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="author")

    starred = models.BooleanField(default=False)

    objects = AuthorManager()

    class Meta:
        unique_together = (("first_name", "last_name"),)
        default_related_name = "author"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=Author)
@receiver(post_delete, sender=Author)
def reset_author_cache(*args, **kwargs):
    print("Resetting authors cache")
    cache.delete("authors")
