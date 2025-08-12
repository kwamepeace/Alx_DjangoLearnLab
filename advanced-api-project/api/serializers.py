from rest_framework import serializers
from .models import Book, Author


#Serializer for the Book model to serialize book data
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Book
        fields = ['title', 'publication_year', 'author']

# A nested serializer for the Author model to include related books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']