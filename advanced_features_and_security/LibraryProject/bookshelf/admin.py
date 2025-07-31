from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin as UserAdmin
from django.contrib.auth.models import Group
from .forms import UserCreationForm, CustomUserChangeForm


class Bookadmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year','author')
    search_fields = ('publication_year', )

# This code registers the Book and BookAdmin model with the Django admin site
admin.site.register(Book, Bookadmin)


class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the CustomUser model.
    This allows us to add custom fields to the user creation and change forms.
    """
    add_form = UserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('username', 'email', 'date_of_birth', 'profile_photo', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_of_birth')
    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ( 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    ]

    add_fieldsets = [
        (None, 
        {   'classes': ['wide'],
            'fields': [ 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo']
            }
        ),
    ]
    search_fields = ('email', 'username', 'date_of_birth')
    ordering = {'email',}   
    filter_horizontal = []

# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)

# Unregister the default Group model to avoid conflicts
# Optional, but if you don't need the Group model, you can unregister it
admin.site.unregister(Group)

