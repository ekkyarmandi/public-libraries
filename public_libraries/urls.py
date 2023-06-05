from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("admin/", views.AdminPage.as_view(), name="admin"),
    path("admin/users/", views.UsersTable.as_view(), name="users"),
    path("admin/books/", views.BooksTable.as_view(), name="books"),
    path("login/", views.LoginPage.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.RegisterPage.as_view(), name="register"),
    path("clear-table/", views.clear_table, name="clear_table"),
]
