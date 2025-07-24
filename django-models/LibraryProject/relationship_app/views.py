from django.shortcuts import render, redirect, get_object_or_404
from .models import Library, Book, Librarian
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import  authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm  
from django.views.generic import DetailView
from django.contrib import messages
from .forms import CustomUserCreationForm, RegisterForm, BookForm
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required



def homepage(request):
    """
    Renders the homepage for the application.
    """
    return render(request, 'relationship_app/homepage.html')

def list_books(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, context)


class LibraryDetailView(DetailView):
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


def is_admin(user):
    """Checks if the user has the 'Admin' role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'AD'

def is_librarian(user):
    """Checks if the user has the 'Librarian' role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'LI'

def is_member(user):
    """Checks if the user has the 'Member' role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'ME'

# --- Role-Based Views ---

@login_required # Ensures user is logged in
@user_passes_test(is_admin, login_url='/login/', redirect_field_name=None)
def admin_view(request):
    """View accessible only to Admin users."""
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

@login_required # Ensures user is logged in
@user_passes_test(is_librarian, login_url='/login/', redirect_field_name=None)
def librarian_view(request):
    """View accessible only to Librarian users."""
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

@login_required # Ensures user is logged in
@user_passes_test(is_member, login_url='/login/', redirect_field_name=None)
def member_view(request):
    """View accessible only to Member users."""
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})




@login_required
def admin_view(request):
    # Example: Check for superuser status or specific group/permission
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('relationship_app:homepage') # Or a different redirect
    return render(request, 'relationship_app/admin_dashboard.html')

@login_required
def librarian_view(request):
    # Example: Check if user belongs to 'Librarians' group or has a specific permission
    if not request.user.groups.filter(name='Librarians').exists():
        messages.error(request, 'You do not have permission to access the librarian dashboard.')
        return redirect('relationship_app:homepage')
    return render(request, 'relationship_app/librarian_dashboard.html')

@login_required
def member_view(request):
    # All logged-in users are generally considered members for this view
    return render(request, 'relationship_app/member_dashboard.html')



@permission_required('relationship_app.can_add_book', raise_exception=True)
@login_required # Often good to combine with login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('relationship_app:book_list') # Redirect to book list
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add'})

@permission_required('relationship_app.can_change_book', raise_exception=True)
@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('relationship_app:book_list') # Redirect to book list
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'book': book, 'action': 'Edit'})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('relationship_app:book_list') # Redirect to book list
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})
