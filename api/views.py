from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.serializers import BookSerializer
from library.filters import BookFilter
from library.models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
