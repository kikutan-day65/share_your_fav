from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)

    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return str(self.username)
