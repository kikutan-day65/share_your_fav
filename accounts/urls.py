from django.urls import path

from .views import (
    UserDetailView,
    UserLoginView,
    UserLogoutView,
    UserRegiserSuccesView,
    UserRegisterView,
)

app_name = "accounts"
urlpatterns = [
    # path("accounts-home/", view_name.as_view(), name="accounts_home"),
    path(
        "user-register/",
        UserRegisterView.as_view(),
        name="user_register",
    ),
    path("user-detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path(
        "user-register-success/",
        UserRegiserSuccesView.as_view(),
        name="user_register_success",
    ),
    path("user-login/", UserLoginView.as_view(), name="user_login"),
    path("user-logout/", UserLogoutView.as_view(), name="user_logout"),
]
