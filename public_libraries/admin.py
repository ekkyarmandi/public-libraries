from django.contrib import admin
from .models import Book, BorrowedBook, BorrowReturnRequest


class BookModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "publisher",
        "language",
        "stock",
        "category",
    )


class BorrowedBookModelAdmin(admin.ModelAdmin):
    list_display = ("related_book", "related_user", "borrowed_date", "is_borrowed", "is_returned")


class BorrowRequest(admin.ModelAdmin):
    list_display = ("related_book", "requested_by", "action", "is_approved")

    def related_book(self, obj):
        try:
            return obj.borrowed_book.related_book
        except:
            return "Borrowed Book Entry Deleted" # Todo: Add related book also to the request model


admin.site.register(Book, BookModelAdmin)
admin.site.register(BorrowedBook, BorrowedBookModelAdmin)
admin.site.register(BorrowReturnRequest, BorrowRequest)
