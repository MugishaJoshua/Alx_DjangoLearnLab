from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# Serializer for Book model.
# Serializers convert model instances into JSON and validate input for API requests.
class BookSerializer(serializers.ModelSerializer):

    # Custom validation for publication_year to ensure it cannot be in the future.
    # DRF automatically calls "validate_<fieldname>" when validating input.
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        # Include all fields in the Book model
        fields = '__all__'


# Serializer for Author model with nested books.
# This serializer not only returns the author's name but also
# serializes all related books using the BookSerializer.
class AuthorSerializer(serializers.ModelSerializer):

    # Nested serializer for the books related to the author.
    # The reverse relationship works because the Book model uses related_name='books'.
    # Setting read_only=True prevents creating books directly inside AuthorSerializer.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        # Only return author name + nested list of books
        fields = ['name', 'books']
