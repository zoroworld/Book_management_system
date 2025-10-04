# apps/books/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer
from django.shortcuts import get_object_or_404, redirect
from django.http import StreamingHttpResponse
from io import BytesIO
from .models import Book
import dropbox
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,AllowAny




# List all books or create a new book
class BookListAPI(APIView):
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated]

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


dbx = dropbox.Dropbox(settings.DROPBOX_OAUTH2_TOKEN)

class BookFileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    lookup_field = 'isbn'  # use ISBN instead of default pk

    @action(detail=True, methods=['get'])
    def pdf(self, request, isbn=None):
        book = get_object_or_404(Book, isbn=isbn)
        if book.book_pdf:
            return redirect(book.book_pdf.url)
        return Response({"detail": "PDF not found"}, status=404)

    @action(detail=True, methods=['get'])
    def cover(self, request, isbn=None):
        book = get_object_or_404(Book, isbn=isbn)
        if book.cover_image:
            return redirect(book.cover_image.url)
        return Response({"detail": "Cover image not found"}, status=404)


    @action(detail=True, methods=['get'], url_path='stream-pdf')
    def stream_pdf(self, request, isbn=None):
        book = get_object_or_404(Book, isbn=isbn)
        if not book.book_pdf:
            return Response({"detail": "PDF not found"}, status=404)

        dropbox_path = f"/media/{book.book_pdf.name}"
        try:
            metadata, res = dbx.files_download(dropbox_path)
            file_like = BytesIO(res.content)
            response = StreamingHttpResponse(file_like, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{book.book_pdf.name.split("/")[-1]}"'
            return response
        except dropbox.exceptions.ApiError as e:
            return Response({"detail": str(e)}, status=404)

