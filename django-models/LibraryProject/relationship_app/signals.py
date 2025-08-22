from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile 


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create or update a UserProfile whenever a User is saved.
    - sender: The model class that sent the signal (in this case, User).
    - instance: The actual instance of the model that was just saved.
    - created: A boolean; True if a new record was created, False if an existing one was updated.
    - kwargs: Additional keyword arguments.
    """
    if created:
        # If a new user is created, create a new UserProfile for them
        UserProfile.objects.create(user=instance)
    else:
        # If an existing user is updated, ensure their UserProfile exists and save it.
        # This handles cases where a user might exist without a profile (e.g., pre-signal users).
        try:
            instance.userprofile.save() # Access the profile using 'userprofile'
        except UserProfile.DoesNotExist:
            # If the profile doesn't exist for an existing user, create it.
            UserProfile.objects.create(user=instance)

