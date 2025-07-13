from django.contrib import admin

# Register your models here.
from .models import Book

admin.site.register(Book)
# This code registers the Book model with the Django admin site