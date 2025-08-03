from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
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
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access



class DeleteBookView(generics.DestroyAPIView):
    """
    A view for deleting a Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]  # Ensure only authenticated users can delete


class ReadOnlyBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Authenticated users can read, but not create/update/delete
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

