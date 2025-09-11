from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect,render ,get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import CATEGORY_CHOICES
from django.db.models import Exists, OuterRef
from .models import Favorite

from .models import Book, Favorite, Author
from .forms import BookForm, BookFilterForm


def apply_filters(request):
    qs = Book.objects.select_related("author").all()
    form = BookFilterForm(request.GET or None)
    if form.is_valid():
        q = form.cleaned_data.get("q")

        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(author__name__icontains=q) | Q(category__icontains=q))
    return qs, form


class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books" 
    paginate_by = 20               

    
    def get_queryset(self):
        qs, _ = apply_filters(self.request)
        if self.request.user.is_authenticated:
            fav_qs = Favorite.objects.filter(user=self.request.user, book=OuterRef("pk"))
            qs = qs.annotate(is_fav=Exists(fav_qs))
        return qs.select_related("author")
    
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = getattr(self, "filter_form", None)
        return ctx

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_forms.html"
    success_url = reverse_lazy("books:book_list")

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_forms.html"
    success_url = reverse_lazy("books:book_list")

class BookDeleteView(DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("books:book_list")


@login_required
def toggle_favorite(request, pk):
    book = Book.objects.get(pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if not created:
        fav.delete()
        messages.info(request, "removed from favorits")
    else:
        messages.success(request, "added to Favs")
    return redirect("books:book_list")


class MyFavoritesListView(LoginRequiredMixin, ListView):
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginatie_by = 20
    def get_queryset(self):
        fav_qs = Favorite.objects.filter(user=self.request.user, book=OuterRef("pk"))
        return (
            Book.objects.select_related("author")
            .annotate(is_fav=Exists(fav_qs)) 
            .filter(is_fav=True)              
            .order_by("-created_at")
        )
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = None
        ctx["favorites_view"] = True
        return ctx

class AuthorDetailView(DetailView):
    model = Author
    template_name = "books/author_detail.html"
    context_object_name = "author"
