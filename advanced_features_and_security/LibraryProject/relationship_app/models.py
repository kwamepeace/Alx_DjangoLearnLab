from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
