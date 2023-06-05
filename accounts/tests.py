from django.test import TestCase
from django.urls import reverse
from .models import Account


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create(
            fullname="Test User",
            username="testuser",
            email="test@mail.com",
            password="testpassword",
        )

    def test_account_fullname(self):
        acc = Account.objects.get(id=1)
        self.assertEqual(acc.fullname, "Test User")

    def test_account_username(self):
        acc = Account.objects.get(id=1)
        self.assertEqual(acc.username, "testuser")

    def test_account_email(self):
        acc = Account.objects.get(id=1)
        self.assertEqual(acc.email, "test@mail.com")
