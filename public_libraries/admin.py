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
    list_display = ("related_book", "related_user", "borrowed_date", "is_returned")


class BorrowRequest(admin.ModelAdmin):
    list_display = ("borrowed_book", "requested_by", "action", "is_approved")


admin.site.register(Book, BookModelAdmin)
admin.site.register(BorrowedBook, BorrowedBookModelAdmin)
admin.site.register(BorrowReturnRequest, BorrowRequest)
