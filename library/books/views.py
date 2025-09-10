from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect,render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import CATEGORY_CHOICES

from .models import Book, Favorite, Author
from .forms import BookForm, BookFilterForm

def apply_filters(request):
    qs = Book.objects.select_related("author").all()
    form = BookFilterForm(request.GET or None)
    if form.is_valid():
        q = form.cleaned_data.get("q")
        author = form.cleaned_data.get("author")
        category = form.cleaned_data.get("category")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        from_date = form.cleaned_data.get("from_date")
        to_date = form.cleaned_data.get("to_date")

        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(author__name__icontains=q))
        if author:
            qs = qs.filter(author=author)
        if category:
            qs = qs.filter(category=category)
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        if from_date:
            qs = qs.filter(published_date__gte=from_date)
        if to_date:
            qs = qs.filter(published_date__lte=to_date)
    return qs, form




class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books" 
    paginate_by = 20               
    # queryset = Book.objects.select_related('author').all() 

    # def get_queryset(self):
    #     qs, _ = apply_filters(self.request)
    #     return qs
    def get_queryset(self):
        qs, form = apply_filters(self.request)
        self.filter_form = form                 # ذخیره برای get_context_data
        return qs.order_by("id") 
    
    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     _, form = apply_filters(self.request)
    #     ctx["filter_form"] = form
    #     return ctx
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = getattr(self, "filter_form", None)
        return ctx

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_forms.html"
    success_url = reverse_lazy("books:book_list")

# class BookUpdateView(UpdateView):
#     model = Book
#     form_class = BookForm
#     template_name = "books/book_form.html"
#     success_url = reverse_lazy("books:book_list")

# class BookDeleteView(DeleteView):
#     model = Book
#     template_name = "books/book_confirm_delete.html"
#     success_url = reverse_lazy("books:book_list")

# def bulk_delete_filtered(request):
#     if request.method == "POST":
#         class DummyReq: GET = request.POST
#         qs, _ = apply_filters(DummyReq)
#         count = qs.count()
#         qs.delete()
#         messages.success(request, f"{count} books removed")
#     return redirect("books:book_list")

# @login_required
# def toggle_favorite(request, pk):
#     book = Book.objects.get(pk=pk)
#     fav, created = Favorite.objects.get_or_create(user=request.user, book=book)
#     if not created:
#         fav.delete()
#         messages.info(request, "removed from favorits")
#     else:
#         messages.success(request, "added to Favs")
#     return redirect("books:book_list")

# class MyFavoritesListView(LoginRequiredMixin, ListView):
#     template_name = "books/book_list.html"
#     context_object_name = "books"
#     def get_queryset(self):
#         return Book.objects.filter(favorited_by__user=self.request.user).select_related("author")
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx["filter_form"] = None
#         ctx["favorites_view"] = True
#         return ctx

# class AuthorDetailView(DetailView):
#     model = Author
#     template_name = "books/author_detail.html"
#     context_object_name = "author"




# def (request):
#     if request.method == 'POST':
#         form = RegistrationForm()
#         if form.is_valid():
#             Registration.objects.create(**form.cleaned_data)
#             return HttpResponse("OK")
#     else:
#         form = RegistrationForm()
#     return HttpResponse( )

from django.views.generic import DetailView
from .models import Author

class AuthorDetailView(DetailView):
    model = Author
    template_name = "books/author_detail.html"
    context_object_name = "author"
