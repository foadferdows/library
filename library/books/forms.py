from django import forms
from .models import Book, Author , User
import django_jalali.forms as jforms
from django_jalali.admin.widgets import AdminjDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



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




# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ("username" , "email" , "password1" , "password2")

#     def clean_email(self):
#         email = self.cleaned_data["email"].strip().lower()
#         if User.objects.filter(email__iexact=email).exists():
#             raise forms.ValidationError("Duplicat email founded")
#         return email
    
#     def save(self, commit = True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data["email"].strip().lower()
#         if commit:
#             user.save()
#         return user

