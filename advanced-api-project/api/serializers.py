from rest_framework import serializers
from .models import Book, Author


#Serializer for the Book model to serialize book data
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Book
        fields = ['title', 'publication_year', 'author']

    # def validate(self, data):
    #     """
    #     Custom validation to ensure publication year is not in the future.
    #     """
    #     if data['publication_year'] > 2025 and len(data['title']) < 5:
    #         raise serializers.ValidationError("Publication year cannot be in the future.")

# A nested serializer for the Author model to include related books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']