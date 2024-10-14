from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")


class CustomUserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]
