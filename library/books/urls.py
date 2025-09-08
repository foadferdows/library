from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("books/new/", views.BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/edit/", views.BookUpdateView.as_view(), name="book_update"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
    path("bulk-delete/", views.bulk_delete_filtered, name="bulk_delete_filtered"),

    path("fav/<int:pk>/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/", views.MyFavoritesListView.as_view(), name="my_favorites"),

]
