from django.test import TestCase
from .models import Book  # Assuming you have a Book model
from rest_framework import status
from rest_framework.test import APITestCase  # Correctly import APITestCase from DRF
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


# This is a standard Django test class for a non-API model
class BookModelTests(TestCase):
    def setUp(self):
        """
        Create test books for the model tests.
        """
        Book.objects.create(title="Empire", publication_year=1879)
        Book.objects.create(title="The richest man in Babylon", publication_year=2020)

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
        Set up users and a URL for testing API permissions.
        """
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='testpassword'
        )
        self.protected_url = reverse('books/')

    def test_unauthenticated_request_is_unauthorized(self):
        """
        Ensure unauthenticated users are denied access.
        This method must be indented inside the class.
        """
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_access_is_forbidden(self):
        """
        Ensure a regular user is denied access to an admin-only view.
        This method must be indented inside the class.
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_access_is_allowed(self):
        """
        Ensure an admin user is granted access.
        This method must be indented inside the class.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
