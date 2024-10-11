from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView

from .forms import CustomAuthenticationForm, CustomUserRegisterForm
from .models import CustomUser


# Create your views here.
class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserRegisterForm
    template_name = "accounts/user_register_form.html"
    success_url = reverse_lazy("accounts:register_success_page")


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "accounts/user_detail.html"
    context_object_name = "user_detail"
