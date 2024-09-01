from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import CustomAuthenticationForm


# Create your views here.
class MyLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"
