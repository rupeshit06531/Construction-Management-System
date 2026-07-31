from django.urls import path

from .views import (
    MaterialListCreateAPIView,
    MaterialDetailAPIView,
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