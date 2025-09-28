# apps/books/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookListAPI, BookDetailAPI, BookFileViewSet

router = DefaultRouter()
router.register(
    r'',
    BookFileViewSet,
    basename='book-files'
)
router.lookup_value_regex = '[^/]+'

urlpatterns = [
    path('list', BookListAPI.as_view(), name='api_book_list'),
    path('<str:isbn>', BookDetailAPI.as_view(), name='api_book_detail'),
    path('', include(router.urls)),
]

# http://localhost:8000/api/v1/books/ff029b74dd6a48b8a093db3da51d9957/pdf/
# http://localhost:8000/api/v1/books/ff029b74dd6a48b8a093db3da51d9957/cover/
# http://localhost:8000/api/v1/books/ff029b74dd6a48b8a093db3da51d9957/stream-pdf/
