from django.contrib.auth import login
from django.urls import reverse_lazy 
from django.shortcuts import redirect, reverse


from django.views.generic import FormView
from django.contrib import messages
from .forms import SignUpForm

class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("books:book_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)    
        messages.success(self.request, "loggin successfuly !!!")
        return super().form_valid(form)

# def logoutview(request):
#     base = reverse("books:book_list")
#     return f"{base}"