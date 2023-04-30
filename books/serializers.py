from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from books.models import Book, Country, Author, Order, OrderLineItem
from customers.models import Customer

import time


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)
    average_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Author
        fields = ("first_name", "last_name", "books_count", "average_price")


class AuthorBooksSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def create(self, validated_data):
        authors = validated_data.pop("authors")

        with transaction.atomic():
            book = super().create(validated_data)

            for author in authors:
                book.authors.add(author)

            return book

    class Meta:
        model = Book
        fields = ("id", "name", "price", "authors")


class BookSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)

    serializer_method_field = serializers.SerializerMethodField("calculate_field")

    # tags = serializers.SerializerMethodField("get_tags")

    # def get_tags(self, book):
    #     # Imagine that we get tags from somewhere
    #     # response = requests.get("https://example.com/tags")
    #     # return response.json()
    #     # For testing purposes we will sleep instead of making a request
    #     time.sleep(0.1)
    #
    #     return ["tag1", "tag2"]

    def calculate_field(self, book):
        return f"This is some string of book {book.name}"

    class Meta:
        model = Book
        fields = ("id", "name", "country", "authors", "seller", "authors_string", "serializer_method_field",
                  "count_sold", "price")


class OrderLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLineItem
        fields = ('book', 'quantity')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("email", "phone_number")


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "name")


class OrderSerializer(serializers.ModelSerializer):
    line_items = OrderLineItemSerializer(many=True)
    customer = CustomerSerializer()
    books = SimpleBookSerializer(many=True, read_only=True)

    def create(self, validated_data):
        customer_data = validated_data['customer']

        customer, _ = Customer.objects.update_or_create(
            email=customer_data["email"],
            defaults={"phone_number": customer_data["phone_number"]}
        )

        validated_data['customer'] = customer

        line_items = validated_data.pop("line_items")

        with transaction.atomic():
            order = super().create(validated_data)

            updated_books = []

            for line_item in line_items:
                # [{"book": <Book: 1>, "quantity": 5], {"book": <Book: 2>, "quantity": 10]}
                book = line_item["book"]
                quantity = line_item["quantity"]
                OrderLineItem.objects.create(book=book, order=order, quantity=quantity)

                book.count_sold += quantity
                updated_books.append(book)

            for book in updated_books:
                book.save()

        return order

    class Meta:
        model = Order
        fields = ("id", "line_items", "customer", "books")


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
