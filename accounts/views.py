from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Create your views here.
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("main")
    template_name = "accounts/signup.html"
