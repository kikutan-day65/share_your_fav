from django.urls import path

from .views import LikeView, LocationDataView, LocationFormView, Map

app_name = "map"
urlpatterns = [
    path("", Map.as_view(), name="map"),
    path("location-form/", LocationFormView.as_view(), name="location_form"),
    path("location-data/<int:pk>/", LocationDataView.as_view(), name="location_data"),
    path("like/<int:location_id>/", LikeView.as_view(), name="like"),
]
