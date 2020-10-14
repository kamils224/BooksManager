from django.urls import path
from .views import books_crud, books_import

urlpatterns = [
    path('', books_crud.BookList.as_view(), name='index'),
    path('library/', books_crud.BookList.as_view()),
    path('library/<str:title>/<str:author>/<str:language>/<str:release_date_min>/<str:release_date_max>',
         books_crud.BookList.as_view()),
    path('library/create/', books_crud.BookCreate.as_view(), name='create'),
    path('library/update/<int:pk>', books_crud.BookUpdate.as_view(), name='update'),
    path('library/delete/<int:pk>', books_crud.BookDelete.as_view(), name='delete'),
    path('library/books_import/', books_import.index, name='books_import'),
]
