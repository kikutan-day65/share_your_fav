from django.urls import path

from .views import (
    LocationCreateView,
    LocationDeleteView,
    LocationDetailView,
    LocationUpdateView,
    MapView,
)

app_name = "location"
urlpatterns = [
    path("map/", MapView.as_view(), name="map"),
    path(
        "location-create-form/",
        LocationCreateView.as_view(),
        name="location_create_form",
    ),
    path(
        "location-detail/<int:pk>/",
        LocationDetailView.as_view(),
        name="location_detail",
    ),
    path(
        "location-update-form/<int:pk>/",
        LocationUpdateView.as_view(),
        name="location_update_form",
    ),
    path(
        "location-delete/<int:pk>/",
        LocationDeleteView.as_view(),
        name="location_delete",
    ),
]
