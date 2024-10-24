from django.urls import path

from .views import LocationCreateView, MapView

app_name = "location"
urlpatterns = [
    path("map/", MapView.as_view(), name="map"),
    path(
        "location-create-form/",
        LocationCreateView.as_view(),
        name="location_create_form",
    ),
]
