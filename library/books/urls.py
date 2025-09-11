from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import *

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("books/new/", BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book_update"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
    path("bulk-delete/", views.bulk_delete_books, name="bulk_delete_books"), 
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),

    path("fav/<int:pk>/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/", MyFavoritesListView.as_view(), name="my_favorites"),

]
