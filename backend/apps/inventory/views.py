from drf_spectacular.utils import extend_schema
from rest_framework import generics

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Inventory
from .serializers import InventorySerializer


@extend_schema(
    tags=["Inventory"],
    summary="List and create inventory records",
    description=(
        "GET: Retrieve inventory records.\n"
        "POST: Create a new inventory record."
    ),
)
class InventoryListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):
    queryset = Inventory.objects.select_related(
        "material",
    ).order_by("-created_at")

    serializer_class = InventorySerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "POST": IsAdminOrManager,
    }


@extend_schema(
    tags=["Inventory"],
    summary="Inventory details",
    description=(
        "Retrieve, update or delete a single inventory record."
    ),
)
class InventoryDetailAPIView(
    RolePermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = Inventory.objects.select_related(
        "material",
    )

    serializer_class = InventorySerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }