from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

from .forms import CustomAuthenticationForm


# Create your views here.
class MyLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"
    next_page = "home:home"


class MyLogoutView(LogoutView):
    next_page = "accounts:login"
