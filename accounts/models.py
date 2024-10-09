from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, validators=[MinLengthValidator(5)]
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return str(self.username)
