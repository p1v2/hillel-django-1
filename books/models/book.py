from django.db import models
from django.contrib.auth.models import User
from books.models import Author, Country


class Book(models.Model):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author, blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE, blank=True)
    price = models.FloatField(null=True)
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    count_selled = models.IntegerField(null=True)
    is_archived = models.BooleanField(null=True)


    @property
    def authors_string(self):
        authors_names = []

        for author in self.authors.all():
            authors_names.append(f"{author.first_name} {author.last_name}")

        return ", ".join(authors_names)

    def __str__(self):
        return f'This book is {self.name} it has {self.pages_count} pages, it author is {self.authors} ' \
               f'Made in {self.country} ' \
               f'The price is {self.price} Seller is {self.seller}'
    def get_information(self, book_name : str):
        self.book = Book.objects.select_related('country').prefetch_related('authors').get(name=book_name)
        author_full_name = [[a.first_name, a.last_name] for a in self.book.authors.all()]
        book_info = {
            'name': self.book.name,
            'pages_count': self.book.pages_count,
            'authors': [' '.join(a) for a in author_full_name],
            'country': self.book.country.name if self.book.country_id else'no-info',
            'price': self.book.price,
            'seller': self.book.seller.username if self.book.seller_id else 'no-info',
        }
        return book_info
