from django.contrib import admin
from .models import Book, BorrowedBook


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


admin.site.register(Book, BookModelAdmin)
admin.site.register(BorrowedBook, BorrowedBookModelAdmin)
