from django.urls import path

from .views import LocationFormView, Map

app_name = "map"
urlpatterns = [
    path("", Map.as_view(), name="map"),
    path("location-form/", LocationFormView.as_view(), name="location_form"),
]
