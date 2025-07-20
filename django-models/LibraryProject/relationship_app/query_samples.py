from relationship_app.models import Author, Book, Library, Librarian  


def query_book_by_author(author):
    author = Author.objects.get(name=author)
    author_books = Book.objects.filter(author=author)
    return f"{author.name} has written the following books: {', '.join(book.title for book in author_books)}"


def list_all_books_in_library(library_name):
    all_books = ['Library.objects.get(name=library_name).name', "books.all()"]
    return all_books


def retrieve_librarian_from_library(library_name):
    name = Librarian.object.get(name = library_name)
    return f"The librarian for {library_name} is {name.name}" 
 