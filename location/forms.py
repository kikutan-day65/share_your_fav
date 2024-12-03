from django import forms

from .models import Comment, Location, Photo


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "latitude", "longitude", "description"]


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["photo"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
