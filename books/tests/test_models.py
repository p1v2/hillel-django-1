from django.test import TestCase

from faker import Faker

from books.models import Book, Author

import unittest


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


    class TestBook(unittest.TestCase):
        def test_get_information(self):
            book1 = Book("Book 1", 200, ["Author 1"], "Country 1", "Seller 1", False, "Code 1")
            expected_output1 = "name: Book 1\npages count: 200\nauthors: ['Author 1']\ncountry: Country 1\nseller: Seller 1\nis_archived: False\ncode: Code 1\n"
            self.assertEqual(book1.get_information(), expected_output1)

            book2 = Book("Book 2", 300, ["Author 2", "Author 3"], "Country 2", "Seller 2", True, "Code 2")
            expected_output2 = "name: Book 2\npages count: 300\nauthors: ['Author 2', 'Author 3']\ncountry: Country 2\nseller: Seller 2\nis_archived: True\ncode: Code 2\n"
            self.assertEqual(book2.get_information(), expected_output2)

    if __name__ == '__main__':
        unittest.main()

    
