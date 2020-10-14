import django_filters

from library.models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    language = django_filters.CharFilter(lookup_expr='icontains')
    date_gt = django_filters.NumberFilter(field_name='date', lookup_expr='gt')
    date__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Book
        fields = ['title', 'author', 'release_date', 'language']
