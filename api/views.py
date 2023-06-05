from rest_framework import viewsets
from public_libraries.models import Book, BorrowedBook, BorrowReturnRequest
from public_libraries.serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView


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
        books = []
        # get user unprocessed requests
        user_requests = BorrowReturnRequest.objects.filter(
            requested_by=request.user, is_approved=False, is_rejected=False
        )
        for r in user_requests:
            books.append(
                {
                    "id": r.related_book.id,
                    "stock": r.related_book.stock,
                    "status": "pending",
                }
            )
        # get user borrowed books
        user_borrowed_books = BorrowedBook.objects.filter(
            related_user=request.user, is_returned=False
        )
        for r in user_borrowed_books:
            if r.related_book.id not in [b["id"] for b in books]:
                books.append(
                    {
                        "id": r.related_book.id,
                        "stock": r.related_book.stock,
                        "status": "borrowed",
                    }
                )
        # return the book id and it's status
        return Response(books)

    def patch(self, request, *args, **kwargs):
        book = Book.objects.get(id=kwargs["pk"])
        if book.stock > 0:  # check book stock availability
            # check number of books borrowed by user
            try:
                borrowed = BorrowedBook.objects.filter(
                    related_user=request.user, is_returned=False
                )
                borrowed = [b.related_book for b in borrowed]
            except:
                borrowed = []

            # check max. number of books that can be borrowed
            if len(borrowed) == 3:
                return Response(
                    {"message": "You can only borrow 3 books."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # check if user alread requested to borrow this book or not
            try:
                request = BorrowReturnRequest.objects.get(
                    requested_by=request.user,
                    related_book=book,
                    action="borrow",
                    is_approved=False,
                )
                return Response(
                    {"message": "You already requested to borrow this book."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except:
                pass

            # check if user already borrowed this book or not
            if len(borrowed) <= 3 and book not in borrowed:
                BorrowReturnRequest.objects.create(
                    borrowed_book=BorrowedBook.objects.create(
                        related_book=book, related_user=request.user
                    ),
                    related_book=book,
                    requested_by=request.user,
                    action="borrow",
                )
                return Response(
                    {"message": "Request sent to admin."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "You already borrowed this book."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": "Book is out of stock."}, status=status.HTTP_400_BAD_REQUEST
            )


class ReturnBook(GenericAPIView):
    def patch(self, request, *args, **kwargs):
        book = Book.objects.get(id=kwargs["pk"])
        try:
            # borrowed_book = BorrowedBook.objects.get(
            #     related_book=book, related_user=request.user, is_returned=False
            # )
            # borrowed_book.is_returned = True
            # borrowed_book.returned_date = timezone.now()
            # borrowed_book.save()
            # book.stock += 1
            # book.save()
            # serializer = BookSerializer(book, many=False)
            # return Response(serializer.data)

            # Todo: Make a request to admin
            return Response(
                {"message": "Request sent to admin."},
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            return Response(
                {"message": "You didn't borrow this book.", "error": str(err)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AdminHandleRequest(GenericAPIView):
    def patch(self, request, *args, **kwargs):
        request_id = kwargs["pk"]
        admin_action = request.data.get("action", "")
        request_entries = BorrowReturnRequest.objects.get(id=request_id)
        if admin_action == "approve":
            request_entries.is_approved = True
            request_entries.borrowed_book.is_borrowed = True
            request_entries.related_book.stock -= 1
            request_entries.related_book.save()
            request_entries.borrowed_book.save()
            request_entries.save()
        elif admin_action == "reject":
            request_entries.is_rejected = True
            request_entries.borrowed_book.delete()
            request_entries.save()
        return Response(
            {"message": "Request handled successfully."},
            status=status.HTTP_200_OK,
        )
