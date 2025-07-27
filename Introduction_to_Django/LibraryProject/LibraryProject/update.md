Book.objects.filter(title ="1984").update(title = "Nineteen Eighty-Four")
OR
book = Book.objects.get(title = "1984")
book.title = "Nineteen Eighty-Four"
book.save()

"""
This will update the book name from 1984 to Nineteen Eighty-Four
"""