from django.urls import path
from . import views
urlpatterns = [
    path("catalog/", views.BookViewSet.as_view({"get": "list"}), name="book-list"),
    path("catalog/borrow/<str:pk>/", views.BorrowBook.as_view(), name="borrow-book"),
    path("catalog/return/<str:pk>/", views.ReturnBook.as_view(), name="return-book"),
]
