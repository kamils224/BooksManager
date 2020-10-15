import django_filters

from library.models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    language = django_filters.CharFilter(lookup_expr='icontains')
    release_date_min = django_filters.DateFilter(field_name='release_date', lookup_expr='gte')
    release_date_max = django_filters.DateFilter(field_name='release_date', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['title', 'author', 'release_date', 'language']
