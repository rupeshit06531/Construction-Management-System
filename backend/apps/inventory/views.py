from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Inventory
from .serializers import InventorySerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Inventory"],
    summary="List and create inventory",
    description=(
        "GET: Retrieve inventory records with search, filtering and ordering.\n"
        "POST: Add a new inventory record."
    ),
)
class InventoryListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):

    queryset = Inventory.objects.select_related(
        "material"
    ).all()

    serializer_class = InventorySerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "material__name",
        "material__unit",
    ]

    filterset_fields = [
        "material",
    ]

    ordering_fields = [
        "created_at",
        "quantity",
    ]

    ordering = [
        "-created_at",
    ]

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
        "material"
    ).all()

    serializer_class = InventorySerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }