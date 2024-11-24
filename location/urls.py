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
        "create-form/",
        LocationCreateView.as_view(),
        name="create_form",
    ),
    path(
        "<int:pk>/detail/",
        LocationDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/update-form/",
        LocationUpdateView.as_view(),
        name="update_form",
    ),
    path(
        "<int:pk>/delete/",
        LocationDeleteView.as_view(),
        name="delete",
    ),
]
