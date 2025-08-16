from django.test import TestCase
from .models import Book, Author  
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()



# This is a standard Django test class for a non-API model
class BookModelTests(TestCase):
    def setUp(self):
        """
        Create test books for the model tests.
        """
        self.author = Author.objects.create(name="Example Author")
        Book.objects.create(title="Empire", publication_year=1879, author=self.author)
        Book.objects.create(title="The richest man in Babylon", publication_year=2020, author=self.author)

    def test_book_creation(self):
        """
        Test that Book objects are created with the correct data.
        """
        book_1 = Book.objects.get(title="Empire")
        book_2 = Book.objects.get(title="The richest man in Babylon")

        self.assertEqual(book_1.publication_year, 1879)
        self.assertEqual(book_1.title, "Empire")
        self.assertEqual(book_2.title, "The richest man in Babylon")
        self.assertEqual(book_2.publication_year, 2020)


# This is a Django REST Framework test class for API views
class MyAPIViewTests(APITestCase):
    def setUp(self):
        """
        Set up users, a URL, and a book for testing API permissions and data.
        """
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='testpassword'
        )
        self.author = Author.objects.create(name="F. Scott Fitzgerald")
        # Assuming 'books/' is a named URL for the list view
        self.list_url = reverse('books/')
        self.book_data = {'title': 'The Great Gatsby', 'publication_year': 1925, 'author': self.author.pk}
        self.existing_book = Book.objects.create(title="Empire", publication_year=1879, author=self.author)

    def test_unauthenticated_request_is_unauthorized(self):
        """
        Ensure unauthenticated users are denied access.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_access_is_forbidden(self):
        """
        Ensure a regular user is denied access to an admin-only view.
        """
        self.client.login(user=self.regular_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_access_is_allowed(self):
        """
        Ensure an admin user is granted access.
        """
        self.client.login(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_books_returns_correct_data(self):
        """
        Ensure the book list view returns the correct serialized data.
        This test uses `response.data`.
        """
        self.client.login(user=self.admin_user)
        Book.objects.create(title="The richest man in Babylon", publication_year=2020, author=self.author)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Checks that both books are returned
        
        # Check the data content of the first book
        self.assertEqual(response.data[0]['title'], 'Empire')
        self.assertEqual(response.data[0]['publication_year'], 1879)
        self.assertEqual(response.data[0]['author'], self.author.pk)
        
        # Check the data content of the second book
        self.assertEqual(response.data[1]['title'], 'The richest man in Babylon')
        self.assertEqual(response.data[1]['publication_year'], 2020)
        self.assertEqual(response.data[1]['author'], self.author.pk)

    def test_create_book_with_valid_data_succeeds(self):
        """
        Ensure a new book can be created with a POST request and the correct data is returned.
        This test also uses `response.data`.
        """
        self.client.login(user=self.admin_user)
        response = self.client.post(self.list_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2) # Now 2 books exist in the database

        # Check the data returned in the response
        self.assertEqual(response.data['title'], 'The Great Gatsby')
        self.assertEqual(response.data['publication_year'], 1925)
        self.assertEqual(response.data['author'], self.author.pk)


    def test_create_book_with_future_year_fails(self):
        """
        Ensure that a book cannot be created with a publication year in the future.
        """
        self.client.login(user=self.admin_user)
        future_year = date.today().year + 1
        invalid_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.pk
        }
        response = self.client.post(self.list_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertEqual(response.data['publication_year'][0], "Publication year cannot be in the future.")


    def test_update_book_with_valid_data_succeeds(self):
        """
        Ensure a book can be updated with a PUT request and the changes are reflected.
        This test uses `response.data`.
        """
        self.client.login(user=self.admin_user)
        # Assuming there is a detail view URL like 'book-detail'
        detail_url = reverse('book-detail', args=[self.existing_book.pk])
        updated_data = {'title': 'Updated Title', 'publication_year': 2024, 'author': self.author.pk}
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reload the book instance from the database to check for changes
        self.existing_book.refresh_from_db()
        self.assertEqual(self.existing_book.title, 'Updated Title')
        self.assertEqual(self.existing_book.author, self.author) # Check the model instance
        
        # Check the data returned in the response
        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['publication_year'], 2024)
        self.assertEqual(response.data['author'], self.author.pk)

    def test_delete_book_succeeds(self):
        """
        Ensure a book can be deleted with a DELETE request.
        """
        self.client.login(user=self.admin_user)
        # Assuming there is a detail view URL like 'book-detail'
        detail_url = reverse('book-detail', args=[self.existing_book.pk])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0) # Check if the book is gone
