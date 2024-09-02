from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email", max_length=255)


class SignUpForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
