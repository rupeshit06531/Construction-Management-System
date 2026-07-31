from django.urls import path

from .views import (
    InventoryListCreateAPIView,
    InventoryDetailAPIView,
)


urlpatterns = [
    path(
        "",
        InventoryListCreateAPIView.as_view(),
        name="inventory-list-create",
    ),

    path(
        "<int:pk>/",
        InventoryDetailAPIView.as_view(),
        name="inventory-detail",
    ),
]