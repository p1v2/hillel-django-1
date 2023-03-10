from django.contrib.auth.models import User
from django.db import models
from books.models import Author
from books.models import Country


class Book(models.Model):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author, blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE, blank=True)
    price = models.FloatField()
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_archived = models.BooleanField(null=True, default=False)
    count_selled = models.IntegerField(null=True)
    count_sold = models.IntegerField(default=0)

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