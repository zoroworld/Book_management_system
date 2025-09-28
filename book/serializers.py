from rest_framework import serializers
from book.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn','title', 'price', 'author','genre' ,'cover_image', 'book_pdf']