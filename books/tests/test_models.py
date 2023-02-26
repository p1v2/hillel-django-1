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

        self.country = Country.objects.create(name=random.choice(['Ukraine', 'Poland', 'Germany']))

        self.user = User.objects.create(username=fake.user_name())
    # def test_authors_string_zero_authors(self):
    #     authors_string = self.book.authors_string
    #
    #     self.assertEqual(authors_string, "")
    #
    # def test_authors_string_one_author(self):
    #     self.book.authors.add(self.author1)
    #
    #     authors_string = self.book.authors_string
    #
    #     self.assertEqual(authors_string, f"{self.author1.first_name} {self.author1.last_name}")
    #
    # def test_authors_string_multiple_authors(self):
    #     self.book.authors.add(self.author1, self.author2)
    #
    #     authors_string = self.book.authors_string
    #
    #     self.assertEqual(authors_string,
    #                      f"{self.author1.first_name} {self.author1.last_name}, "
    #                      f"{self.author2.first_name} {self.author2.last_name}")

    def test_book_get_information_name(self):
        name_info = self.book.get_information("Кобзар").get('name')

        self.assertEqual(name_info, 'Кобзар')

    def test_book_get_information_name_str_int(self):
        int_name = random.choice(range(1, 9, 1))
        self.book.name = int_name
        self.book.save()

        name_info = self.book.get_information(str(int_name)).get('name')

        self.assertEqual(name_info, str(int_name))

    def test_book_get_information_null_pages_count(self):
        pages_count = self.book.get_information("Кобзар").get('pages_count')

        self.assertEqual(pages_count, None)

    def test_book_get_information_int_pages_count(self):
        pages = random.choice(range(50, 500, 10))
        self.book.pages_count = pages
        self.book.save()

        pages_count = self.book.get_information("Кобзар").get('pages_count')

        self.assertEqual(pages_count, pages)

    def test_book_get_information_no_country(self):
        country_info = self.book.get_information("Кобзар").get('country')

        self.assertEqual(country_info, 'no data')

    def test_book_get_information_country(self):
        self.book.country = self.country
        self.book.save()

        country_info = self.book.get_information("Кобзар").get('country')

        self.assertEqual(country_info, self.country.name)

    def test_book_get_information_price(self):
        price = random.choice(range(100, 1000, 100))
        self.book.price = price
        self.book.save()
        price_info = self.book.get_information("Кобзар").get('price')

        self.assertEqual(price_info, price)

    def test_book_get_information_count_sold(self):
        count_sold = random.choice(range(1, 100, 1))
        self.book.count_sold = count_sold
        self.book.save()
        count_sold_info = self.book.get_information("Кобзар").get('count_sold')

        self.assertEqual(count_sold_info, count_sold)

    def test_book_get_information_is_archive(self):
        bools = [True, False]
        is_archived = random.choice(bools)
        self.book.is_archived = is_archived

        is_archived_info = self.book.get_information("Кобзар").get('is_archived')

        self.assertEqual(is_archived_info, is_archived_info)

    def test_book_get_information_is_archive_null(self):
        self.book.is_archived = None
        self.book.save()

        is_archived_info = self.book.get_information("Кобзар").get('is_archived')

        self.assertEqual(is_archived_info, is_archived_info)

    def test_book_get_information_authors_empty(self):
        authors_info = self.book.get_information("Кобзар").get('authors')

        self.assertEqual(authors_info, [])

    def test_book_get_information_authors_one(self):
        self.book.authors.add(self.author1)
        authors_info = self.book.get_information("Кобзар").get('authors')

        self.assertEqual(authors_info, [f"{self.author1.first_name} {self.author1.last_name}"])

    def test_book_get_information_authors_multiple(self):
        self.book.authors.add(self.author1, self.author2)
        authors_info = self.book.get_information("Кобзар").get('authors')

        self.assertEqual(authors_info, [f"{self.author1.first_name} {self.author1.last_name}",
                                        f"{self.author2.first_name} {self.author2.last_name}"])

    def test_book_get_information_seller(self):
        self.book.seller = self.user
        self.book.save()

        seller_info = self.book.get_information("Кобзар").get('seller')

        self.assertEqual(seller_info, self.user.username)

    def test_book_get_information_seller_null(self):
        seller_info = self.book.get_information("Кобзар").get('seller')

        self.assertEqual(seller_info, 'no data')