from django.test import TestCase
from .models import Book
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class APITestCase(TestCase):
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






class MyAPIViewTests(APITestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='testpassword'
        )
        self.protected_url = reverse('my-protected-view')



def test_unauthenticated_request_is_unauthorized(self):
        """
        Ensure unauthenticated users are denied access.
        """
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def test_regular_user_access_is_forbidden(self):
        """
        Ensure a regular user is denied access to an admin-only view.
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

def test_admin_user_access_is_allowed(self):
    """
    Ensure an admin user is granted access.
    """
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.get(self.protected_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)