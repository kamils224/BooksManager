from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='index'),
    path('library/', views.BookList.as_view(), name='index'),
    path('library/create/', views.BookCreate.as_view(), name='create'),
    path('library/update/<int:pk>', views.BookUpdate.as_view(), name='update'),
    path('library/delete/<int:pk>', views.BookDelete.as_view(), name='delete'),
]