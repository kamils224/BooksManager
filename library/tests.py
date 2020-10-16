from django.test import TestCase
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist

from library.models import Book


class BookTestCase(TestCase):
    def setUp(self) -> None:
        Book.objects.create(title='Book1', author='Author1', release_date='2010-10-10',
                            isbn_number='12345678910123', pages=50, cover_url='http://example.com',
                            language='pl')
        Book.objects.create(title='Book2', author='Author2', release_date='1995-05-01',
                            isbn_number='0000000000', pages=50, cover_url='http://example2.com',
                            language='en')

    def testBookStr(self) -> None:
        book_1 = Book.objects.get(title='Book1')
        book_2 = Book.objects.get(author='Author2')
        self.assertEqual(str(book_1), f'{book_1.title}/{book_1.author}'
                                      f'/{book_1.release_date}/{book_1.isbn_number}/{book_1.pages}'
                                      f'/{book_1.cover_url}/{book_1.language}')
        self.assertEqual(str(book_2), f'{book_2.title}/{book_2.author}'
                                      f'/{book_2.release_date}/{book_2.isbn_number}/{book_2.pages}'
                                      f'/{book_2.cover_url}/{book_2.language}')


class BookViewsTestCase(TestCase):
    def setUp(self) -> None:
        Book.objects.create(title='Any Book1', author='Author1', release_date='2010-10-10',
                            isbn_number='12345678910123', pages=50, cover_url='http://example.com',
                            language='pl')
        Book.objects.create(title='Book2 example', author='Author2', release_date='1995-05-01',
                            isbn_number='0000000000', pages=50, cover_url='http://example2.com',
                            language='en')

    def test_index(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_context_books_count(self) -> None:
        response = self.client.get('/')
        self.assertEqual(len(response.context['books']), 2)

    def test_pagination(self) -> None:
        response_p1 = self.client.get('/?page=1')
        response_p2 = self.client.get('/?page=2')
        self.assertEqual(response_p1.status_code, HTTPStatus.OK)
        self.assertEqual(response_p2.status_code, HTTPStatus.NOT_FOUND)

    def test_filters_title(self) -> None:
        title_1 = 'book1'
        title_2 = 'book3'
        response_1 = self.client.get(f'/?title={title_1}')
        response_2 = self.client.get(f'/?title={title_2}')

        self.assertEqual(response_1.status_code, HTTPStatus.OK)
        self.assertEqual(len(response_1.context['books']), 1)

        self.assertEqual(response_2.status_code, HTTPStatus.OK)
        self.assertEqual(len(response_2.context['books']), 0)

    def test_filters_author(self) -> None:
        author_1 = 'author1'
        author_2 = 'author3'
        response_1 = self.client.get(f'/?author={author_1}')
        response_2 = self.client.get(f'/?author={author_2}')

        self.assertEqual(response_1.status_code, HTTPStatus.OK)
        self.assertEqual(len(response_1.context['books']), 1)

        self.assertEqual(response_2.status_code, HTTPStatus.OK)
        self.assertEqual(len(response_2.context['books']), 0)

    def test_filters_min_date(self) -> None:
        date_min_1 = '1950-05-05'
        date_min_2 = '2030-05-05'
        response_1 = self.client.get(f'/?release_date_min={date_min_1}')
        response_2 = self.client.get(f'/?release_date_min={date_min_2}')

        self.assertEqual(response_1.status_code, HTTPStatus.OK)
        self.assertEqual(len(response_1.context['books']), 2)

        self.assertEqual(response_2.status_code, HTTPStatus.OK)
        self.assertEqual(len(response_2.context['books']), 0)

    def test_filters_max_date(self) -> None:
        date_max_1 = '1950-05-05'
        date_max_2 = '2030-05-05'
        response_1 = self.client.get(f'/?release_date_max={date_max_1}')
        response_2 = self.client.get(f'/?release_date_max={date_max_2}')

        self.assertEqual(response_1.status_code, HTTPStatus.OK)
        self.assertEqual(len(response_1.context['books']), 0)

        self.assertEqual(response_2.status_code, HTTPStatus.OK)
        self.assertEqual(len(response_2.context['books']), 2)

    def test_library_fail(self) -> None:
        response = self.client.get('/library/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_library_create_get(self) -> None:
        response = self.client.get('/library/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_library_create_post(self) -> None:
        response = self.client.post('/library/create/',
                                    data={
                                        'title': 'new book',
                                        'author': 'new author',
                                        'release_date': '2020-10-20',
                                        'isbn_number': '1231231231',
                                        'pages': 5,
                                        'cover_url': 'http://example.com',
                                        'language': 'de'
                                    }, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        created = Book.objects.get(title='new book', author='new author',
                                   release_date='2020-10-20', isbn_number='1231231231',
                                   pages=5, cover_url='http://example.com', language='de')

        self.assertTrue(isinstance(created, Book))

    def test_library_update_get(self) -> None:
        response = self.client.get('/library/update/1')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_library_update_post(self) -> None:
        response = self.client.post('/library/update/1',
                                    data={
                                        'title': 'update book',
                                        'author': 'update author',
                                        'release_date': '2020-10-20',
                                        'isbn_number': '1231231231',
                                        'pages': 15,
                                        'cover_url': 'http://example.com',
                                        'language': 'de'
                                    }, follow=True)
        updated_object = Book.objects.get(id=1)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(updated_object.title, 'update book')

    def test_library_update_fail(self) -> None:
        response = self.client.get('/library/update/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_library_delete_get(self) -> None:
        # get delete should do nothing
        objects_count_before = len(Book.objects.all())
        response = self.client.get('/library/delete/1')
        objects_count_after = len(Book.objects.all())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(objects_count_before, objects_count_after)

    def test_library_update_post(self) -> None:
        response = self.client.post('/library/delete/1',
                                    data={
                                        'title': 'update book',
                                        'author': 'update author',
                                        'release_date': '2020-10-20',
                                        'isbn_number': '1231231231',
                                        'pages': 15,
                                        'cover_url': 'http://example.com',
                                        'language': 'de'
                                    }, follow=True)
        try:
            deleted_object = Book.objects.get(id=1)
        except ObjectDoesNotExist:
            deleted_object = None
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(deleted_object, None)

    def test_library_delete_fail(self) -> None:
        response = self.client.get('/library/delete/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
