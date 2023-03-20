from django.db import models

from books.models.author_profile import AuthorProfile


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    profile = models.OneToOneField(AuthorProfile, on_delete=models.SET_NULL, null=True, related_name="author")

    starred = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
