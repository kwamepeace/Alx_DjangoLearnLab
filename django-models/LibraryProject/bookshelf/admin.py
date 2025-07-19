from django.contrib import admin
from .models import Book


class Bookadmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year','author')
    search_fields = ('publication_year', )



admin.site.register(Book, Bookadmin)
# This code registers the Book and BookAdmin model with the Django admin site