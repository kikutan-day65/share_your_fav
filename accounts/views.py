from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, SignUpForm


# Create your views here.
class MyLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"
    next_page = "home:home"


class MyLogoutView(LogoutView):
    next_page = "accounts:login"


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:login")
