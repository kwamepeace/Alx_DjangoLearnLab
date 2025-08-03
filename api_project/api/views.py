from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer

from .models import Book

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
