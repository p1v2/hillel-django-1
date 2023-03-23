from django.core.management import BaseCommand
from django.db.models import Q

from books.models import Book


# from django.db.models import Q, Prefetch
#
# from books.models import Book, Author, Order, GiftPackaging


class Command(BaseCommand):
    def handle(self, *args, **options):
        # # Usual way to get all books
        # books = Book.objects.all()

        # Get iterator of all books
        # books_iterator = Book.objects.order_by("name").iterator(chunk_size=10)
        # for book in books_iterator:
        #     print(book.name)
        #     input("Continue?")
        #
        # # Slicing of books
        # books = Book.objects.all()[990:1000]
        #
        # Get SQL expression
        # sql = Book.objects.all()[990:1000].query
        # print(sql)

        # Select only id and name from book
        # query_with_only = Book.objects.only("id", "name").query
        # print(query_with_only)
        # books = Book.objects.order_by("id").only("id", "name")
        # for book in books:
        #     print(book.__dict__)
        #     print(book.name)
        #     print(book.price)
        #     input("Continue?")

        # Select only id and name from book
        # books_values = Book.objects.values("id", "name")[:10]
        #
        # for book_value in books_values:
        #     print(book_value["author__first_name"])

        # books = Book.objects.filter(country__name="Ukraine").select_related("country").prefetch_related("authors")
        # for book in books:
        #     print(book.authors.all()[0].first_name)
        #     print(book.country)

        # Values list
        # books = list(Book.objects.values_list("name", flat=True).order_by("name"))
        # print(books)

        # books = Book.objects.defer("name")
        # print(books[0].__dict__)

        # OR filtering
        # query = "Alicia"
        # filter_expressions = [
        #     Q(name__contains=query),
        #     Q(authors__first_name=query),
        #     Q(authors__last_name=query)
        # ]

        # expression = Q("False")
        # for filter_expression in filter_expressions:
        #     expression |= filter_expression
        #
        # print(expression)

        # books = Book.objects.filter(Q(name__contains=query) | Q(authors__first_name=query) | Q(authors__last_name=query))
        # print(books)

        # Not filtering
        # books = Book.objects.exclude(name__contains="Alicia")
        # via ~ operator
        # books = Book.objects.filter(~Q(name__contains="Alicia"))
        # print(books)
        #
        # # Complex expressions with Q
        # books = Book.objects.filter(~(Q(name__contains="Alicia") & Q(authors__first_name="Alicia")))
        # print(books.query)
        #
        # # Subqueries
        # authors_names = Author.objects.values_list("first_name", flat=True)
        # print(authors_names)
        # authors = Author.objects.filter(first_name="Мирон")
        # print([author.last_name for author in authors])
        # books = Book.objects.filter(authors__in=authors)
        # print(books.query)
        #
        # # Bulk create, bulk update
        # book1 = Book(name="Book 1", price=100)
        # book2 = Book(name="Book 2", price=200)
        # book3 = Book(name="Book 3", price=300)
        #
        # Book.objects.bulk_create([book1, book2, book3], batch_size=1000)
        #
        # # Bulk update
        # Book.objects.filter(name__contains="Book").update(price=1000)
        # # SQL: UPDATE "books_book" SET "price" = 1000 WHERE "books_book"."name" LIKE %Book%
        #
        # book1.price = 100
        # book2.price = 200
        # book3.price = 300
        #
        # Book.objects.bulk_update([book1, book2, book3], ["price"], batch_size=1000)

        # Update concrete book
        # book = Book.objects.get(name="Book 1")
        # book.price = 100
        # book.save()

        # Create via objects manager
        # book = Book.objects.create(name="Book 1", price=100)
        # Create via model
        # book = Book(name="Book 1", price=100)
        # book.save()

        # Bulk delete
        # Book.objects.filter(name__contains="Book").delete()
        # SQL: DELETE FROM "books_book" WHERE "books_book"."name" LIKE %Book%

        # Delete by id
        # book = Book.objects.get(name="Book 1")
        # book.delete()

        # Get first result
        # Bad way
        # book = Book.objects.all()[0]
        # SQL: Select * from books_book

        # book = Book.objects.filter(name="Invalid name")[0]
        # print(book)

        # Good way
        # book = Book.objects.filter(name="Invalid name").first()
        # print(book)

        # Get last result
        # book = Book.objects.last()
        # print(book)

        # Get last result by name
        # book = Book.objects.latest("name")
        # print(book)

        # Get first result by name
        # book = Book.objects.earliest("name")
        # print(book)
        #
        # # Get random result
        # book = Book.objects.order_by("?").first()
        #
        # # Order by different fields one ascending and one descending
        # # Using - for descending
        # books = Book.objects.order_by("name", "-price", "authors__first_name")

        # Exists query
        # exist_book = Book.objects.filter(authors__first_name="Мирон").exists()
        # print(exist_book)
        #
        # # Count query
        #
        # # Bad way
        # books = Book.objects.filter(authors__first_name="Мирон")
        # count_books = len(books)
        #
        # # Good way
        # count_books = Book.objects.filter(authors__first_name="Мирон").count()

        # # Get distinct values
        # first_names = Book.objects.values("authors__first_name").distinct()
        # print(first_names)
        #
        # # Get distinct prices
        # Book.objects.all().distinct("price")

        # Raw query
        # books = Book.objects.raw("SELECT * FROM books_book limit 1")
        # print(list(books))

        # book.delete()

        # # Prefetch to specific field
        # books = Book.objects.prefetch_related(Prefetch("starred_authors", queryset=Author.objects.filter(starred=True)))
        #
        # for book in books:
        #     print(book.authors.all())
        #     print(book.starred_authors.all())

        # # Explain query
        # books_explain = Book.objects.filter(authors__first_name="Мирон").explain(ANALYZE=True)
        # print(books_explain)

        # Select related when using nested relations
        # books_with_packaging = Order.objects.select_related("packaging", "packaging__giftpackaging").all()

        # gift_packagings = GiftPackaging.objects.all().select_related("packaging_ptr", "packaging_ptr__order")

        # Union query
        # Select all books that have name "Alicia" or "Kobzar"
        books = Book.objects.filter(name__contains="Alicia").union(Book.objects.filter(name__contains="Kobzar"))
        # Using filter with or
        books = Book.objects.filter(Q(name__contains="Alicia") | Q(name__contains="Kobzar"))
        print(books)

        # Intersection query
        # Select all books that have author Vitalii and have name "Alicia"
        Book.objects.filter(authors__first_name="Vitalii").intersection(Book.objects.filter(name__contains="Alicia"))

        # Difference query
        # Select all books that have author Vitalii and don't have name "Alicia"
        Book.objects.filter(authors__first_name="Vitalii").difference(Book.objects.filter(name__contains="Alicia"))
