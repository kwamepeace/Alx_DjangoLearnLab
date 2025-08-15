from rest_framework import serializers
from .models import Book, Author
from datetime import date


# Serializer for the Book model to serialize book data
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validate_publication_year(self, data):
        """
        Custom validation for the publication_year field.
        """
        if data > date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return data

# A nested serializer for the Author model to include related books
class AuthorSerializer(serializers.ModelSerializer):
    # This field uses the related_name from the Book model
    books = BookSerializer(many=True, read_only=True, source='book_set')

    class Meta:
        model = Author
        fields = ['name', 'books']