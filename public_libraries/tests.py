from django.test import TestCase
from django.urls import reverse
from accounts.models import Account
from .models import Book

class BorrowRetrunBookTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # create book data
        Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="123456789",
            publisher="Test Publisher",
            number_of_page=123,
            language="English",
            stock=3,
            category="Test Category",
            image_url="https://testurl.com",
            description="Test Description",
        )

        # create user data
        Account.objects.create(
            username="testuser",
            fullname="Test User",
            email="test@mail.com",
            password="testpassword",
        )

    def test_borrow_book_request(self):
        # login user
        self.client.login(email="test@mail.com", password="testpassword")

        # get book id
        book_id = Book.objects.get(title="Test Book").id

        # send borrow request
        response = self.client.patch(
            reverse("borrow-book", kwargs={"pk": book_id})
        )

        # check if borrow request is successful
        self.assertEqual(response.status_code, 200)
