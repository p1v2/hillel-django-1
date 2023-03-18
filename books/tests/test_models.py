import random

from django.test import TestCase

from faker import Faker

from books.models import Book, Author, Country
from django.contrib.auth.models import User


class BookTestCase(TestCase):
    def setUp(self) -> None:
        fake = Faker()
        self.book = Book.objects.create(name="Кобзар", price=100)

        self.author1 = Author.objects.create(first_name=fake.first_name(), last_name=fake.last_name())
        self.author2 = Author.objects.create(first_name=fake.first_name(), last_name=fake.last_name())

        self.country = Country.objects.create(name=random.choice(['Germany', 'Poland', 'Ukraine']))
        self.user = User.objects.create(username=fake.user_name())

    def test_authors_string_zero_authors(self):
        authors_string = self.book.authors_string

        self.assertEqual(authors_string, "")

    def test_authors_string_one_author(self):
        self.book.authors.add(self.author1)

        authors_string = self.book.authors_string

        self.assertEqual(authors_string, f"{self.author1.first_name} {self.author1.last_name}")

    def test_authors_string_multiple_authors(self):
        self.book.authors.add(self.author1, self.author2)

        authors_string = self.book.authors_string

        self.assertEqual(authors_string,
                         f"{self.author1.first_name} {self.author1.last_name}, "
                         f"{self.author2.first_name} {self.author2.last_name}")

    def test_get_information(self):
        book_test_info = self.book.get_information()
        self.assertEqual(book_test_info,
                         "Book's name is Cobsar\nCountry is Netherlands\nCount of pages: 228\nPrice is 700")