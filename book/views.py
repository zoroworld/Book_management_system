# apps/books/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from django.shortcuts import get_object_or_404

# List all books or create a new book
class BookListAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({'message': f"fetching the books." , "data":serializer.data}, status=status.HTTP_201_CREATED)


    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f"Book is created." , "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a specific book
class BookDetailAPI(APIView):
    def get_object(self, isbn):
        return get_object_or_404(Book, isbn=isbn)

    def get(self, request, isbn):
        book = self.get_object(isbn)
        if not book:
            return Response(
                {"message": f"Book not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookSerializer(book)
        return Response({'message': f"Book is fetch." ,"data": serializer.data } , status=status.HTTP_200_OK, )

    def put(self, request, isbn):
        book = self.get_object(isbn)
        if not book:
            return Response(
                {"message": f"Book not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f"Book is update" , "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, isbn):
        print(request)
        book = self.get_object(isbn)
        if not book:
            return Response(
                {"message": f"Book not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        book.delete()
        return Response(
            {"message": f"Book with book isbn {isbn} has been deleted."},
            status=status.HTTP_204_NO_CONTENT
        )
