from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import BookSerializer

from .models import Book

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for performing CRUD operations on Book instances using default actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
