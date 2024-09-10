from django.urls import path

from .views import LocationView, Map

app_name = "map"
urlpatterns = [
    path("", Map.as_view(), name="map"),
    path("location-form/", LocationView.as_view(), name="location_form"),
]
