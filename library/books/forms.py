from django import forms
from .models import Book, Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "category", "price", "published_date", "description"]

class BookFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search")
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label="author")
    min_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label="lower price")
    max_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label="max price")
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":"date"}), label="from ( publish date )")
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":"date"}), label="to ( publish date )")
