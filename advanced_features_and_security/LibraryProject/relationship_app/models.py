from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Needed for settings.AUTH_USER_MODEL

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    class Meta:
        # These custom permissions are correctly defined and match your views.py decorators.
        permissions = (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    # Each library has one librarian, and vice-versa, or a librarian is linked to one library.
    # OneToOneField is appropriate if one Library has exactly one Librarian.
    library = models.OneToOneField(Library, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name
    
# Define your CustomUser BEFORE UserProfile if UserProfile references it
# This placement is fine as settings.AUTH_USER_MODEL handles the reference.
class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    Adds date_of_birth and profile_photo fields.
    """
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    class Meta:
        # Custom permissions for the CustomUser model.
        permissions = (
            ("can_view_library", "Can view library"),
            ("can_manage_books", "Can manage books"),
        )

class UserProfile(models.Model):
    """
    Stores additional profile information for CustomUser, specifically the role.
    """
    # CORRECTED: Short codes for roles to match views.py checks ('AD', 'LI', 'ME')
    ROLE_CHOICES = [
        ('AD', 'Admin'),
        ('LI', 'Librarian'),
        ('ME', 'Member'),
    ]
    
    # OneToOneField to link a UserProfile to a single CustomUser instance.
    # settings.AUTH_USER_MODEL is used to reference the currently active user model.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Corrected max_length to 2 to match the length of the role codes ('AD', 'LI', 'ME').
    # Default role for new profiles is 'ME' (Member).
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='ME')

    def __str__(self):
        # String representation for the UserProfile, useful in admin.
        return f'{self.user.username} Profile'