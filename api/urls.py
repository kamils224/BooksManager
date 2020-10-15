from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views


router = DefaultRouter()
router.register(r'books', views.BookList)


urlpatterns = [
    path('', include(router.urls))
]