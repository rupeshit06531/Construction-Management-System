from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Material
from .serializers import MaterialSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Materials"],
    summary="List and create materials",
    description=(
        "GET: Retrieve materials with search, filtering and ordering.\n"
        "POST: Add a new material record."
    ),
)
class MaterialListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):

    queryset = Material.objects.select_related(
        "project"
    ).all()

    serializer_class = MaterialSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "name",
        "description",
        "unit",
    ]

    filterset_fields = [
        "project",
    ]

    ordering_fields = [
        "created_at",
        "quantity",
        "price",
    ]

    ordering = [
        "-created_at",
    ]

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "POST": IsAdminOrManager,
    }


@extend_schema(
    tags=["Materials"],
    summary="Material details",
    description=(
        "Retrieve, update or delete a single material record."
    ),
)
class MaterialDetailAPIView(
    RolePermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):

    queryset = Material.objects.select_related(
        "project"
    ).all()

    serializer_class = MaterialSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }