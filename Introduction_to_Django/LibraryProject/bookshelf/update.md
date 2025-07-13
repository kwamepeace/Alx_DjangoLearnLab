Book.objects.filter(title ="1984").update(title = "Nineteen Eighty-Four")
OR
update_title = Book.objects.get(title = "1984")
update_title.title = "Nineteen Eighty-Four"
update_title.save()

"""
This will update the book name from 1984 to Nineteen Eighty-Four
"""