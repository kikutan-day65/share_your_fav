from django.urls import path

from .views import (
    CommentFormView,
    LikeView,
    LocationCreateView,
    LocationDeleteView,
    LocationDetailView,
    LocationUpdateView,
    MapView,
    PhotoFormView,
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
        name="delete"
    ),
    path("<int:pk>/like/", LikeView.as_view(), name="like"),
    path("<int:pk>/comment-form/", CommentFormView.as_view(), name="comment_form"),
    path("<int:pk>/photo-form/", PhotoFormView.as_view(), name="photo_form"),
]
