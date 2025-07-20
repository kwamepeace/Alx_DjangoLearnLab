from relationship_app.models import Author, Book, Library, Librarian  


def query_book_by_author(author_name):
    selected_author = Author.objects.get(name=author_name)
    return f"{selected_author.name} has written the following books: {', '.join(book.title for book in selected_author.book_set.all())}"


all_books = Book.objects.all()
all_authors = Author.objects.all()
all_libraries = Library.objects.all()
all_librarians = Librarian.objects.all()