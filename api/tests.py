from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase

from api.serializers import BookSerializer
from library.models import Book


class BookApiTests(APITestCase):

    def setUp(self) -> None:
        Book.objects.create(title='Book1', author='Author1', release_date='2010-10-10',
                            isbn_number='12345678910123', pages=50, cover_url='http://example.com',
                            language='pl')
        Book.objects.create(title='Book2', author='Author2', release_date='1995-05-01',
                            isbn_number='0000000000', pages=50, cover_url='http://example2.com',
                            language='en')

    def test_book_get_list(self) ->None:
        url = reverse('books-list')
        response = self.client.get(url, format='json')
        items_count = len(Book.objects.all())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), items_count)

    def test_book_get_item(self) -> None:
        id = 1
        url = reverse('books-detail', args=(id,))
        response = self.client.get(url, format='json')
        item = Book.objects.get(id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], item.id)

    def test_book_create(self) -> None:
        url = reverse('books-list')
        items_before_count = len(Book.objects.all())
        response = self.client.post(url, data={'title': 'book3', 'author': 'author3',
                                               'release_date': '2030-05-10',
                                               'isbn_number': '123321', 'pages': 100,
                                               'cover_url': 'http://example2.com',
                                               'language': 'en'}, format='json')
        items_after_count = len(Book.objects.all())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(items_after_count, items_before_count + 1)

    def test_book_update(self) -> None:
        item_id = 1
        url = reverse('books-detail', args=(item_id,))
        data = {'title': 'book3',
                'author': 'author3',
                'release_date': '2030-05-30',
                'isbn_number': '123321',
                'pages': 100, 'cover_url': 'http://example2.com',
                'language': 'en'}
        response = self.client.put(url, data=data, format='json')
        item = Book.objects.get(id=item_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(item.title, response.data['title'])
        self.assertEqual(item.author, response.data['author'])
        self.assertEqual(str(item.release_date), response.data['release_date'])
        self.assertEqual(item.isbn_number, response.data['isbn_number'])
        self.assertEqual(item.pages, response.data['pages'])
        self.assertEqual(item.language, response.data['language'])

    def test_book_delete(self) -> None:
        item_id = 1
        url = reverse('books-detail', args=(item_id,))
        items_before_count = len(Book.objects.all())
        response = self.client.delete(url, format='json')
        items_after_count = len(Book.objects.all())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(items_after_count, items_before_count - 1)
