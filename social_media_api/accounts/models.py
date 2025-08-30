from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    A custom user model that extends Django's AbstractUser.
    Adds a biography, profile picture, and a self-referencing
    Many-to-Many field for followers.
    """
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # The 'followers' field is a ManyToMany relationship to the User model itself.
    # symmetrical=False is crucial here because following is not a two-way relationship
    # (if A follows B, B does not necessarily follow A).
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.username