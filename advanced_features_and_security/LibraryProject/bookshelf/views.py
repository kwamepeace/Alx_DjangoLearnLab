from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.decorators import permission_required, login_required
from .forms import ExampleForm


@permission_required('bookshelf.can_view_book', raise_exception=True)
@login_required
def book_list(request):
    # Logic to retrieve and display books
    books = Book.objects.all()
    return render(request, 'bookshelf/view_books.html', {'books': books})

@permission_required('bookshelf.can_create_book', raise_exception=True)
@login_required
def create_book(request):
    # Logic to create a new book
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'bookshelf/create_book.html')

@permission_required('bookshelf.can_edit_book', raise_exception=True)
@login_required
def edit_book(request, book_id):
    # Logic to edit an existing book
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'bookshelf/edit_book.html', {'book': book})

@permission_required('bookshelf.can_delete_book', raise_exception=True)
@login_required
def delete_book(request, book_id):
    # Logic to delete a book
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf:view_books')
    return render(request, 'bookshelf/delete_book.html', {'book': book})