from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import Library, Book, Librarian
from django.contrib import messages
from .forms import CustomUserCreationForm

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
    

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}. You can now log in.')
            # Use the full URL name with namespace for redirect
            return redirect('relationship_app:login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})