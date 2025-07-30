from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class LibraryAdmin(admin.ModelAdmin):
    list_display = ["name", ]

admin.site.register(Library, LibraryAdmin)


class CustomUserAdmin(UserAdmin):
    # Add custom fields to the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # Add custom fields to the change user form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # Add custom fields to the list display
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')

    # Optionally add custom fields to search fields
    search_fields = ('email', 'first_name', 'last_name', 'date_of_birth')

    # Optionally add custom fields to list filters
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_of_birth')


# Unregister the default User model admin, if it was registered
# This might not be strictly necessary if you never registered the default User,
# but it's good practice to ensure no conflicts if you inherit from AbstractUser
try:
    admin.site.unregister(CustomUser) # If CustomUser was registered directly without a custom admin
except admin.sites.NotRegistered:
    pass

# Register your CustomUser model with your CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)