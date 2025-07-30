from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin


class Bookadmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year','author')
    search_fields = ('publication_year', )



admin.site.register(Book, Bookadmin)
# This code registers the Book and BookAdmin model with the Django admin site

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