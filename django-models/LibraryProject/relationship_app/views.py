from django.shortcuts import render, redirect
from .models import Library, Book, Librarian
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required

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