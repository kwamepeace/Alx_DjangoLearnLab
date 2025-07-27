from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
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
    role_choice =[
        ('Admin' , 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices = role_choice, default='Member')

class CustomUser(AbstractUser):
    
    #A custom user model extending what is in AbsractUser without changing it
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)