import datetime
from typing import Dict, List

import dateparser
import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from ..dtos import BookDto
from ..forms import BooksImportApiForm
from ..models import Book


def index(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        context = {'browse_api_form': BooksImportApiForm()}
        return render(request, 'books_import/index.html', context)
    elif request.method == 'POST':

        if request.POST['action'] == 'browse':
            context = {'browse_api_form': BooksImportApiForm(request.POST),
                       'books': _get_api_objects(_query_from_browse_api_form(request))}
            return render(request, 'books_import/index.html', context)

        elif request.POST['action'] == 'import':
            api_objects = _get_api_objects(_query_from_browse_api_form(request))
            objects_to_add = [Book(title=obj.title,
                                   author=obj.author,
                                   release_date=_parse_date(obj.release_date),
                                   isbn_number=obj.isbn_number,
                                   pages=obj.pages,
                                   cover_url=obj.cover_url,
                                   language=obj.language) for obj in api_objects]
            Book.objects.bulk_create(objects_to_add)
            context = {'browse_api_form': BooksImportApiForm(),
                       'books': api_objects}
            return redirect('index')


BASE_URL = 'https://www.googleapis.com/books/v1/volumes'


def _parse_date(date_string: str) -> datetime.date:
    return dateparser.parse(date_string, date_formats=['%Y-%m-%d']).date()


def _query_from_browse_api_form(request: HttpRequest) -> str:
    q = request.POST.get('q')
    params = {
        'intitle': request.POST.get('intitle', ''),
        'inauthor': request.POST.get('inauthor', ''),
        'inpublisher': request.POST.get('inpublisher', ''),
        'subject': request.POST.get('subject', ''),
        'isbn': request.POST.get('isbn', ''),
        'lccn': request.POST.get('lccn', ''),
        'oclc': request.POST.get('oclc', ''),
    }
    params = [':'.join([str(k), v]) for k, v in params.items() if v != '']
    params = '+'.join(params)
    query = '+'.join([f'q={q}', params]) if len(params) > 0 else f'q={q}'
    return query


def _get_api_objects(query: str) -> List[BookDto]:
    results = []
    try:
        response = requests.get(BASE_URL, params=query).json()
        items: Dict = response['items']
        for item in items:
            item_id = item['id']
            volume_info: dict = item['volumeInfo']
            title = volume_info['title']
            author = '\n'.join(volume_info['authors'])
            release_date = volume_info['publishedDate']

            # note: get ISBN13 or ISBN10 number if possible else take first element
            isbn_number = [identifier for identifier in volume_info['industryIdentifiers']
                           if identifier['type'] == 'ISBN_13' or identifier['type'] == 'ISBN_10']
            isbn_number = max(isbn_number, key=lambda x: len(x['identifier']))['identifier'] \
                if isbn_number else volume_info['industryIdentifiers'][0]['identifier']

            page_count = int(volume_info['pageCount'])
            cover_url = volume_info['imageLinks']['thumbnail']
            language = volume_info['language']
            results.append(BookDto(item_id,
                                   title,
                                   author,
                                   release_date,
                                   isbn_number, page_count,
                                   cover_url,
                                   language))
        return results
    # temporary solution, add some specific error handler
    except requests.exceptions.RequestException:
        return results
    except KeyError:
        return results
