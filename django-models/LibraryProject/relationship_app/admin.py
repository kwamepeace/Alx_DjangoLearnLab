from django.contrib import admin
from .models import Author, Book, Library, Librarian

# Register your models here.
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name", )


admin.site.register(Library, LibraryAdmin)