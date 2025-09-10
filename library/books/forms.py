from django import forms
from .models import Book, Author
import django_jalali.forms as jforms
from django_jalali.admin.widgets import AdminjDateWidget



class BookForm(forms.ModelForm):
    published_date = jforms.jDateField(
        widget=AdminjDateWidget,
        required=False,
        label="published Date",
    )

    class Meta:
        model = Book
        fields = ["title", "author", "category", "price", "published_date", "description"]
        


class BookFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search")
    # author = forms.CharField( required=False, label="author")
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label="author",widget=forms.Select)
    category = forms.CharField( required=False, label="author")
    min_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label="lower price")
    max_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label="max price")
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":"date"}), label="from ( publish date )")
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":"date"}), label="to ( publish date )")

