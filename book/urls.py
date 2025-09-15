# apps/books/urls.py
from django.urls import path
from .views import BookListAPI, BookDetailAPI

urlpatterns = [
    path('', BookListAPI.as_view(), name='api_book_list'),
    path('<str:isbn>', BookDetailAPI.as_view(), name='api_book_detail'),
]