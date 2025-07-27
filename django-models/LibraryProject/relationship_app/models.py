from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField (max_length=100)

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    

    class Meta:
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
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    



class UserProfile(models.Model):
    ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
]
    # Typing the user to Django default user, which handles fields like username, password, and email 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #Selecting role choices
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='Member')
    

    def __str__(self):
        return f"{self.user.username}'s Profile"
