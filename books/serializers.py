from rest_framework import serializers

from books.models import Book, Country, Author


class CountrySerializer(serializers.ModelSerializer):
    count_selled_books = serializers.IntegerField(read_only=True)
    class Meta:
        model = Country
        fields = ("id", "name", "count_selled_books")


class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)
    average_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Author
        fields = ("first_name", "last_name", "books_count", "average_price")


class BookSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    authors = AuthorSerializer(many=True)

    serializer_method_field = serializers.SerializerMethodField("calculate_field")

    def calculate_field(self, book):
        return f"This is some string of book {book.name}"

    class Meta:
        model = Book
        fields = ("id", "name", "country", "authors", "seller", "authors_string", "serializer_method_field")
