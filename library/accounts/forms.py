from django import forms
from .models import  User
import django_jalali.forms as jforms
from django_jalali.admin.widgets import AdminjDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username" , "email" , "password1" , "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Duplicat email founded")
        return email
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        if commit:
            user.save()
        return user

