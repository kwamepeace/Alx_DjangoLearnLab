from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User

# Create your models here.

class Book (models.Model):
    title = models. CharField(max_length = 200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

class CustomUser(AbstractUser):
    #A custom user model extending what is in AbsractUser without changing it
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user