from dataclasses import dataclass
import datetime


@dataclass
class BookDto:
    id: str
    title: str
    author: str
    release_date: str
    isbn_number: str
    pages: int
    cover_url: str
    language: str

