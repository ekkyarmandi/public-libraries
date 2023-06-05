from rest_framework import viewsets
from accounts.models import Account
from public_libraries.models import Book, BorrowedBook
from public_libraries.serializers import BookSerializer, BorrowedBookSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView, GenericAPIView
from django.utils import timezone


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.GET.get("search", "")
        return Book.objects.filter(title__icontains=query)

    def create(self, request, *args, **kwargs):
        # Disable create operation
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        # Disable delete operation
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BorrowBook(GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            borrowed_books = BorrowedBook.objects.filter(
                related_user=request.user, is_returned=False
            )
            borrowed = [BookSerializer(b.related_book).data for b in borrowed_books]
            return Response(borrowed)
        except:
            return Response([])

    def patch(self, request, *args, **kwargs):
        book = Book.objects.get(id=kwargs["pk"])
        if book.stock > 0:
            try:
                borrowed = BorrowedBook.objects.filter(
                    related_user=request.user, is_returned=False
                )
                borrowed = [b.related_book for b in borrowed]
            except:
                borrowed = []

            if len(borrowed) == 3:
                return Response(
                    {"message": "You can only borrow 3 books."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if len(borrowed) <= 3 and book not in borrowed:
                BorrowedBook.objects.create(
                    related_book=book, related_user=request.user
                )
                book.stock -= 1
                book.save()
                borrowed_book = BorrowedBook.objects.filter(
                    related_user=request.user, is_returned=False
                )
                borrowed = [BookSerializer(b.related_book).data for b in borrowed_book]
                return Response(borrowed, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "You already borrowed this book."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"message": "Book is out of stock."}, status=status.HTTP_404_NOT_FOUND
            )


class ReturnBook(GenericAPIView):
    def patch(self, request, *args, **kwargs):
        book = Book.objects.get(id=kwargs["pk"])
        try:
            borrowed_book = BorrowedBook.objects.get(
                related_book=book, related_user=request.user
            )
            borrowed_book.is_returned = True
            borrowed_book.returned_date = timezone.now()
            borrowed_book.save()
            book.stock += 1
            book.save()
            serializer = BookSerializer(book, many=False)
            return Response(serializer.data)
        except Exception as err:
            return Response(
                {"message": "You didn't borrow this book.", "error": str(err)},
                status=status.HTTP_404_NOT_FOUND,
            )
