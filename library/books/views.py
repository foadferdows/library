from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
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
        self.filter_form = _
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


@login_required
@require_POST
def bulk_delete_books(request):
    selected_ids = request.POST.getlist("selected_ids")


    if not selected_ids:
        messages.warning(request, "noting selected")
        return redirect(_redirect_back_to_list_with_filters(request))

    try:
        with transaction.atomic():
            qs = Book.objects.filter(pk__in=selected_ids)
            deleted_count = qs.count()
            qs.delete()         
            print(deleted_count)
        messages.success(request,f"{deleted_count} was deleted")
    except Exception as e:
        messages.error(request, f"we have a problem : {e}")

    return redirect(_redirect_back_to_list_with_filters(request))


def _redirect_back_to_list_with_filters(request):
    base = reverse("books:book_list")
    q = request.POST.get("q", "") or request.GET.get("q", "")
    category = request.POST.get("category", "") or request.GET.get("category", "")
    params = []
    if q:
        params.append(f"q={q}")
    if category:
        params.append(f"category={category}")
    return f"{base}?{'&'.join(params)}" if params else base
