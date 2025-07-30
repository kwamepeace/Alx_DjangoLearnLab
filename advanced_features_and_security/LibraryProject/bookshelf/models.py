from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.conf import settings # Needed for settings.AUTH_USER_MODEL

# Create your models here.

class Book (models.Model):
    title = models. CharField(max_length = 200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = (
            ("can_view_book", "Can view book"),
            ("can_create_book", "Can create book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        )
        verbose_name = "Book"
        verbose_name_plural = "Books"

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
    
    # Default role for new profiles is 'ME' (Member).
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='ME')

    def __str__(self):
        # String representation for the UserProfile, useful in admin.
        return f'{self.user.username} Profile'
    

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and returns a user with an email, username, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)