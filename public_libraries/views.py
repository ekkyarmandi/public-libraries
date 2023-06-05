from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from accounts.models import Account
from .models import Book, BorrowedBook, BorrowReturnRequest


def clear_table(request):
    Book.objects.all().delete()
    return JsonResponse({"status": "success", "message": "Table cleared successfully"})


class HomePage(View):
    def get(self, request):
        if request.user.is_superuser:
            return redirect("admin")
        elif request.user.is_authenticated:
            page_number = request.GET.get("page", 1)
            query = request.GET.get("search", "")
            books = self.query_books(query)
            if books:
                paginator = Paginator(books, 18)
                page_obj = paginator.get_page(page_number)
                pages = [
                    {"number": i, "url": "/?page={}&search={}".format(i, query)}
                    for i in range(1, page_obj.paginator.num_pages + 1)
                ][:30]
                context = {"books": page_obj, "pages": pages, "total_books": len(books)}
            else:
                context = {"total_books": 0, "pages": [{"number": 1, "url": "/"}]}
            return render(request, "home.html", context)
        else:
            return redirect("login")

    def query_books(self, query):
        try:
            books = Book.objects.filter(title__icontains=query)
            for book in books:
                description = book.description
                if description.lower().strip() == "description":
                    book.description = "No description available"
                if len(description) > 300:
                    book.description = description[:300] + "..."
            return books
        except:
            return None


class AdminPage(View):
    def query_request(self, action):
        try:
            return BorrowReturnRequest.objects.filter(
                action=action, is_approved=False
            )
        except:
            return []

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                borrow_requests = self.query_request("borrow")
                return_requests = self.query_request("return")
                context = {
                    "number_of_books": Book.objects.count(),
                    "number_of_users": Account.objects.count() - 1,
                    "number_of_borrowed": BorrowedBook.objects.filter(
                        is_returned=False, is_borrowed=True
                    ).count(),
                    "number_of_returned": BorrowedBook.objects.filter(
                        is_returned=True
                    ).count(),
                    "borrow_requests": borrow_requests,
                    "return_requests": return_requests,
                }
                return render(request, "admin.html", context)
            else:
                return redirect("home")
        else:
            return redirect("login")


class UsersTable(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                users = Account.objects.all().exclude(is_superuser=True)
                for user in users:
                    user.borrowed_book = user.borrowedbook_set.filter(
                        is_returned=False
                    ).count()
                context = {"users": users}
                return render(request, "admin_users.html", context)
            else:
                return redirect("home")
        return redirect("login")


class BooksTable(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context = {"book": Book.objects.first()}
                return render(request, "admin_books.html", context)
            else:
                return redirect("home")
        return redirect("login")


class LoginPage(View):
    def authenticate(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = Account.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except Account.DoesNotExist:
            return None

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        user = self.authenticate(request)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
        return redirect("login")


class RegisterPage(View):
    def check_email(self, request):
        email = request.POST["email"]
        try:
            Account.objects.get(email=email)
            return True
        except Account.DoesNotExist:
            return False

    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        fullname = request.POST["fullname"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password1"]
        if self.check_email(request):
            messages.error(request, "Email already exists!")
            return redirect("register")
        if password1 == password2:
            Account.objects.create_user(
                username=fullname, email=email, password=password1
            )
            messages.success(request, "Account created successfully")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        return redirect("home")


def logout_view(request):
    logout(request)
    return redirect("login")
