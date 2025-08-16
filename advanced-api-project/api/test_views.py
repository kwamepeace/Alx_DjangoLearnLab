from django.test import TestCase
from .models import Book


class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title="Empire", publication_year=1879)
        Book.objects.create(title="The richest man in Babylon", publication_year=2020)

    def test_book_creation(self):
        book_1 = Book.objects.get(title="Empire")
        book_1 = Book.objects.get(publication_year=1879)
        book_2 = Book.objects.get(title="Empire")
        book_2 = Book.objects.get(publication_year=1879)
        self.assertEqual(book_1.publication_year, 1879)
        self.assertEqual(book_1.title, "Empire")
        self.assertEqual(book_2.title, "The richest man in Babylon")
        self.assertEqual(book_2.publication_year, 2020)


