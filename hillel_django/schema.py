import graphene
from graphql import GraphQLResolveInfo


from books.models import Book
from books.schema import BookType, AuthorType


class Query(graphene.ObjectType):
    books = graphene.List(BookType, first=graphene.Int())
    book_by_name = graphene.Field(BookType, name=graphene.String())
    book = graphene.Field(BookType, id=graphene.Int(), name=graphene.String(), price=graphene.Float())
    authors = graphene.List(AuthorType, first=graphene.Int())

    def resolve_book(self, info: GraphQLResolveInfo, id: int = None, name: str = None, price: float = None):
        if id:
            return Book.objects.filter(id=id).first()
        if name:
            return Book.objects.filter(name=name).first()
        if price:
            return Book.objects.filter(price=price).first()

    def resolve_book_by_name(self, info: GraphQLResolveInfo, name: str):
        return Book.objects.filter(name=name).first()

    def resolve_books(self, info: GraphQLResolveInfo, first: int = None):
        books = Book.objects.all()

        selections = info.field_nodes[0].selection_set.selections

        fields_names = [selection.name.value for selection in selections]

        if "authors" in fields_names:
            books = books.prefetch_related("authors")
        if "country" in fields_names:
            books = books.select_related("country")

        if first:
            return books[:first]
        else:
            return books


class BookMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        price = graphene.Float()

    book = graphene.Field(BookType)

    # Validate data before creating a book
    def validate(self, name: str, price: float):
        if not name:
            raise Exception("Name is required")
        if not price:
            raise Exception("Price is required")

    @classmethod
    def mutate(cls, root, info, name: str, price: float):
        print("Running mutation")
        book = Book.objects.create(name=name, price=price)

        return BookMutation(book=book)


class Mutation(graphene.ObjectType):
    create_book = BookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
