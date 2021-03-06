from django.contrib import admin
from library.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn_number')


admin.site.register(Book, BookAdmin)
