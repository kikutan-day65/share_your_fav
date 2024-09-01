from django.urls import path

from .views import MyLoginView, MyLogoutView

app_name = "accounts"
urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
]
