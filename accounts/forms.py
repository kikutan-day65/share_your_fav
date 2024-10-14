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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and (password != confirm_password):
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
