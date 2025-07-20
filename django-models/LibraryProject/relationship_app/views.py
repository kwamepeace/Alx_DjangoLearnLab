from django.shortcuts import render
from .models import Author, Book, Library, Librarian


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView:
    def __init__(self, library_name):
        self.library_name = library_name

    def get_library(self):
        return Library.objects.get(name=self.library_name)

    def get_books(self):
        return self.get_library().books.all()

    def get_librarian(self):
        return Librarian.objects.get(library=self.get_library())
    
    def render(self, request):
        library = self.get_library()
        books = self.get_books()
        librarian = self.get_librarian()
        return render(request, 'relationship_app/library_detail.html', {
            'library': library,
            'books': books,
            'librarian': librarian
        })