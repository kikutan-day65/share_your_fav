import os
import uuid

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


def photo_upload_to(instance, filename):
    extension = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"
    if instance.location:
        location_name = instance.location.name
    else:
        location_name = "unknown_location"
    return os.path.join("location/photos/", location_name, unique_filename)


class Photo(models.Model):
    photo = models.ImageField(upload_to=photo_upload_to, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(
        "Location", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.photo)
