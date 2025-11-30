from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):

    # Validate that publication_year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class Meta:
        model = Book
        fields = '__all__'


# Serializer for Author model with nested books
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer to include all books by the author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
