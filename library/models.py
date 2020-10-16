from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    author = models.CharField(max_length=100, verbose_name='Author')
    release_date = models.DateField(verbose_name='Release date')
    isbn_number = models.CharField(max_length=20,
                                   verbose_name='ISBN')
    pages = models.IntegerField(verbose_name='Pages')
    cover_url = models.URLField(verbose_name='Cover')
    language = models.CharField(max_length=50, verbose_name='Language')

    def __str__(self):
        return f'{self.title}/{self.author}/{self.release_date}' \
               f'/{self.isbn_number}/{self.pages}/{self.cover_url}/{self.language}'
