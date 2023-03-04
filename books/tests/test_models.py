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
        book = Book.objects.get(name="Кобзар")
        self.assertEqual(book.get_information(), f"{self.book.name}")

    def test_get_information_empty_fields(self):
        book = Book.objects.create(name="Тарас", author='Шевченко', price=777)
        self.assertEqual(book.get_information(), f"{self.book.name} {self.book.authors} {self.book.price}")