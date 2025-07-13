from django.contrib import admin
from .models import Book

admin.site.register(Book)
# This code registers the Book model with the Django admin site