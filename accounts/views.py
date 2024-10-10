from django.shortcuts import render
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, CustomUserRegisterForm
from .models import CustomUser


# Create your views here.
class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserRegisterForm
    template_name = "accounts/user_register_form.html"
    # success_url = "accounts:accounts_home"
