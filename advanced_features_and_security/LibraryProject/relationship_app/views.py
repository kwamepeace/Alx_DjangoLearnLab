from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from .forms import CustomUserCreationForm, BookForm # Ensure these forms are correctly defined
from .models import Library, Book, Librarian, UserProfile # Import all necessary models


def is_admin(user):
    """Checks if the user has the 'AD' (Admin) role in their UserProfile."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'AD'

def is_librarian(user):
    """Checks if the user has the 'LI' (Librarian) role in their UserProfile."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'LI'

def is_member(user):
    """Checks if the user has the 'ME' (Member) role in their UserProfile."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'ME'

# --- Core Application Views ---

def homepage(request):
    """
    Renders the homepage for the application.
    """
    return render(request, 'relationship_app/homepage.html')

def list_books(request):
    """
    Lists all available books.
    """
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    """
    Displays details of a specific library, including its books and librarian.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library' # The Library object will be available as 'library' in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.object is the Library instance retrieved by DetailView (based on pk from URL)
        library = self.object

        # Add related books to the context
        context['books'] = library.books.all()

        # Add related librarian to the context
        try:
            context['librarian'] = Librarian.objects.get(library=library)
        except Librarian.DoesNotExist:
            context['librarian'] = None # Handle case where no librarian is found for this library
        except Librarian.MultipleObjectsReturned:
            # This handles the unlikely case where multiple librarians are linked
            context['librarian'] = Librarian.objects.filter(library=library).first()

        return context


def register(request):
    """
    Handles user registration for CustomUser.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(user=user, role='ME') # Default new users to 'Member' role
            messages.success(request, f'Account created successfully for {user.username}. You can now log in.')
            return redirect('relationship_app:login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# --- Role-Based Dashboard Views ---
# These views are protected by login_required and user_passes_test decorators,
# ensuring only users with the correct role can access them.

@login_required
@user_passes_test(is_admin, login_url='relationship_app:login', redirect_field_name=None)
def admin_dashboard(request):
    """
    View accessible only to Admin users, renders the admin dashboard template.
    Passes 'Admin' role to the template.
    """
    return render(request, 'relationship_app/admin_dashboard.html', {'role': 'Admin'})


@login_required
@user_passes_test(is_librarian, login_url='relationship_app:login', redirect_field_name=None)
def librarian_dashboard(request):
    """
    View accessible only to Librarian users, renders the librarian dashboard template.
    Passes 'Librarian' role to the template.
    """
    return render(request, 'relationship_app/librarian_dashboard.html', {'role': 'Librarian'})


@login_required
@user_passes_test(is_member, login_url='relationship_app:login', redirect_field_name=None)
def member_dashboard(request):
    """
    View accessible only to Member users, renders the member dashboard template.
    Passes 'Member' role to the template.
    """
    return render(request, 'relationship_app/member_dashboard.html', {'role': 'Member'})


# --- Book Management Views (Permissions Required) ---
# These views require specific permissions defined in your model's Meta class.

@permission_required('relationship_app.add_book', raise_exception=True) # Use lowercase app_label.permission_codename
@login_required
def add_book(request):
    """
    Handles adding a new book. Requires 'add_book' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('relationship_app:book_list')
        else:
            messages.error(request, 'Failed to add book. Please check the form.')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add'})


@permission_required('relationship_app.change_book', raise_exception=True) # Use lowercase app_label.permission_codename
@login_required
def edit_book(request, pk):
    """
    Handles editing an existing book. Requires 'change_book' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('relationship_app:book_list')
        else:
            messages.error(request, 'Failed to update book. Please check the form.')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'book': book, 'action': 'Edit'})


@permission_required('relationship_app.delete_book', raise_exception=True) # Use lowercase app_label.permission_codename
@login_required
def delete_book(request, pk):
    """
    Handles deleting a book. Requires 'delete_book' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('relationship_app:book_list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})