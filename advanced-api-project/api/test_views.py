from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints:
    - List, Retrieve, Create, Update, Delete
    - Filtering, Searching, Ordering
    - Permissions and Authentication
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create authors
        self.author1 = Author.objects.create(name='George Orwell')
        self.author2 = Author.objects.create(name='J.K. Rowling')

        # Create books
        self.book1 = Book.objects.create(title='1984', publication_year=1949, author=self.author1)
        self.book2 = Book.objects.create(title='Animal Farm', publication_year=1945, author=self.author1)
        self.book3 = Book.objects.create(title='Harry Potter', publication_year=1997, author=self.author2)

        # API client
        self.client = APIClient()

    # ---------------------
    # Test List and Detail
    # ---------------------
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')

    # ---------------------
    # Test Create (auth)
    # ---------------------
    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author2.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.client.logout()

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {'title': 'New Book', 'publication_year': 2020, 'author': self.author2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---------------------
    # Test Update
    # ---------------------
    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book-update', args=[self.book1.id])
        data = {'title': '1984 Updated', 'publication_year': 1949, 'author': self.author1.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, '1984 Updated')
        self.client.logout()

    # ---------------------
    # Test Delete
    # ---------------------
    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())
        self.client.logout()

    # ---------------------
    # Test Filtering
    # ---------------------
    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=1984'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    # ---------------------
    # Test Searching
    # ---------------------
    def test_search_books_by_author(self):
        url = reverse('book-list') + '?search=Orwell'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ---------------------
    # Test Ordering
    # ---------------------
    def test_order_books_by_year_desc(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1997)  # Harry Potter
