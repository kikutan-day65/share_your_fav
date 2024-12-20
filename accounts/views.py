from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView

from .forms import CustomAuthenticationForm, CustomUserRegisterForm
from .models import CustomUser


# Create your views here.
class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserRegisterForm
    template_name = "accounts/user_register_form.html"
    success_url = reverse_lazy("accounts:user_register_success")


class UserRegiserSuccesView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user_register_success.html"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "accounts/user_detail.html"
    context_object_name = "user_detail"


class UserLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "accounts/user_login.html"

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse("accounts:user_detail", kwargs={"pk": user_id})


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("accounts:user_logout")
    template_name = "accounts/user_logout.html"
