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
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


def photo_upload_to(instance: Location, filename: str) -> str:
    """アップロードされたphotoの保存先パスの生成

    Args:
        instance (Location): Locationオブジェクト
        filename (str): アップロードされたファイル名

    Returns:
        str: 保存先のパス
    """
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


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(
        "Location", related_name="location_likes", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "location")

    def __str__(self):
        return f"{str(self.user)} - {str(self.location)}"


class Comment(models.Model):
    comment = models.TextField(blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(
        "Location", related_name="location_comment", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)
