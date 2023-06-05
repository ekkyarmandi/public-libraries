from rest_framework import serializers
from public_libraries.models import Book, BorrowedBook, BorrowReturnRequest


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = "__all__"


class BorrowReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowReturnRequest
        fields = ["action", "related_book", "is_approved", "is_rejected"]
