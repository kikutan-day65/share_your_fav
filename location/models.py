from django.conf import settings
from django.db import models


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=150)
    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
