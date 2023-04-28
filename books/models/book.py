from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from books.models import Author
from books.models import Country
from books.models.item import Item
from books.models.mixins import CheapMixin


class BookQueryset(models.QuerySet, CheapMixin):
    def starred(self):
        return self.filter(authors__starred=True)

    def sold(self):
        return self.filter(count_sold__gt=0)

    def select_related(self, *fields):
        return super().select_related("country", *fields)

    def with_country(self):
        return self.filter(country__isnull=False)

    def with_country_name(self):
        return self.select_related("country").annotate(country_name=models.F("country__name"))


class BookManager(models.Manager):
    _queryset_class = BookQueryset

    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)

    def create(self, **kwargs):
        kwargs["is_archived"] = False
        return super().create(**kwargs)

    def update(self, **kwargs):
        kwargs["is_archived"] = False
        return super().update(**kwargs)

    def starred(self):
        return self.get_queryset().starred()


class ArchivedBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=True)


class Book(Item):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author, blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE, blank=True)
    price = models.FloatField()
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_archived = models.BooleanField(null=True, default=False)
    count_sold = models.IntegerField(default=0)
    pages_count = models.IntegerField(null=True, db_index=True)
    authors = models.ManyToManyField(Author, blank=True, related_name="books")
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_archived = models.BooleanField(default=False)
    code = models.IntegerField(blank=True, null=True, unique=True)

    objects = BookManager()
    archived_objects = ArchivedBookManager()

    @property
    def authors_string(self):
        authors_names = []

        for author in self.authors.all():
            authors_names.append(f"{author.first_name} {author.last_name}")

        return ", ".join(authors_names)

    def get_information(self, book_name: str):
        self.book = Book.objects.select_related('country').prefetch_related('authors').get(name=book_name)
        info = dict()
        info['name'] = self.book.name
        info['pages_count'] = self.book.pages_count
        info['country'] = self.book.country.name if self.book.country_id else'no data'
        info['price'] = self.book.price
        info['count_sold'] = self.book.count_sold
        info['is_archived'] = self.book.is_archived
        author_full_name = [[a.first_name, a.last_name] for a in self.book.authors.all()]
        info['authors'] = [' '.join(a) for a in author_full_name]
        info['seller'] = self.book.seller.username if self.book.seller_id else 'no data'

        return info

    def __str__(self):
        return self.name

    class Meta:
        db_table = "books"
        ordering = ["-price", "count_sold"]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        index_together = [("country", "name")]
        default_related_name = "books"

        # Do not run migrations for this model
        managed = False


# Model
# signals = []

# def receiver(func):
#    signals.append(func)
#    return func
@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
@receiver(post_save, sender=Author)
@receiver(post_delete, sender=Author)
@receiver(post_save, sender=Country)
@receiver(post_delete, sender=Country)
def reset_book_cache(*args, **kwargs):
    pass
    # print("Resetting books cache")
    # keys = cache.keys('books:*') + cache.keys('book:*')
    # for key in keys:
    #     cache.delete(key)
