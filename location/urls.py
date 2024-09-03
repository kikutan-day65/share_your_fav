from django.urls import path

from .views import Map

urlpatterns = [
    path("", Map.as_view(), name="map"),
]
