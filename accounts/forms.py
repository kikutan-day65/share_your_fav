from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")


class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(CustomUserRegisterForm, self).__init__(*args, **kwargs)
        # 不要なフィールドを削除
        if "usable_password" in self.fields:
            del self.fields["usable_password"]
