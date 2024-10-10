from django.urls import path

from .views import UserRegisterView

app_name = "accounts"
urlpatterns = [
    # path("accounts-home/", view_name.as_view(), name="accounts_home"),
    path(
        "user-register/",
        UserRegisterView.as_view(),
        name="user_register_form.html",
    ),
]
