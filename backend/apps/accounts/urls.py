from django.urls import path

from .views import (
    RegisterAPIView,
    LoginAPIView,
    CurrentUserAPIView,
    PasswordChangeAPIView,
)


urlpatterns = [
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "me/",
        CurrentUserAPIView.as_view(),
        name="current_user",
    ),

    path(
        "password/change/",
        PasswordChangeAPIView.as_view(),
        name="password_change",
    ),
]