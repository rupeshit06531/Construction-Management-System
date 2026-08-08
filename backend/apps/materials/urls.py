from django.urls import path

from .views import (
    MaterialDetailAPIView,
    MaterialListCreateAPIView,
)


urlpatterns = [
    path(
        "",
        MaterialListCreateAPIView.as_view(),
        name="material-list-create",
    ),
    path(
        "<int:pk>/",
        MaterialDetailAPIView.as_view(),
        name="material-detail",
    ),
]