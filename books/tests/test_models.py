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

    def test_get_information_name(self):
        name_info = self.book.get_information('Кобзар').get('name')
        self.assertEqual(name_info, 'Кобзар')

    def test_get_information_pages_count(self):
        pages_info = random.choice(range(1, 99))
        self.book.pages_count = pages_info
        self.book.save()
        pages_count = self.book.get_information('Кобзар').get('pages_count')
        self.assertEqual(pages_count, pages_info)

    def test_get_information_country(self):
        self.book.country = self.country
        self.book.save()
        country_info = self.book.get_information('Кобзар').get('country')
        self.assertEqual(country_info, self.country.name)

    def test_get_information_price(self):
        price = random.choice(range(1, 99))
        self.book.price = price
        self.book.save()
        price_info = self.book.get_information('Кобзар').get('price')
        self.assertEqual(price_info, price)

    def test__get_information_seller(self):
        self.book.seller = self.user
        self.book.save()
        seller_info = self.book.get_information('Кобзар').get('seller')
        self.assertEqual(seller_info, self.user.username)
