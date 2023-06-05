from django.db import models
from accounts.models import Account
import uuid


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=125)
    author = models.CharField(max_length=125, null=True, blank=True)
    isbn = models.CharField(max_length=125, null=True, blank=True)
    publisher = models.CharField(max_length=125, null=True, blank=True)
    number_of_page = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=125, null=True, blank=True)
    stock = models.IntegerField(default=3)
    category = models.CharField(max_length=125)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(default="No description available")

    def __str__(self):
        return self.title


class BorrowedBook(models.Model):
    related_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    related_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    returned_date = models.DateTimeField(null=True, blank=True)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)
    is_borrowed = models.BooleanField(default=False)


class BorrowReturnRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    borrowed_book = models.ForeignKey(BorrowedBook, on_delete=models.SET_NULL, null=True)
    related_book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    requested_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    action = models.CharField(max_length=125)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
