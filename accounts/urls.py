from django.urls import path

from .views import MyLoginView

app_name = "accounts"
urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
]
