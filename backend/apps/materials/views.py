from rest_framework import generics

from apps.common.mixins import RolePermissionMixin
from apps.common.permissions import (
    IsManagerOrAbove,
    IsStaffUser,
    IsSuperAdmin,
)

from .models import Material
from .serializers import MaterialSerializer


class MaterialListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):
    queryset = Material.objects.select_related(
        "project",
    ).order_by("-created_at")

    serializer_class = MaterialSerializer

    role_permissions = {
        "GET": IsStaffUser,
        "POST": IsManagerOrAbove,
    }


class MaterialDetailAPIView(
    RolePermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = Material.objects.select_related(
        "project",
    ).all()

    serializer_class = MaterialSerializer

    role_permissions = {
        "GET": IsStaffUser,
        "PUT": IsManagerOrAbove,
        "PATCH": IsManagerOrAbove,
        "DELETE": IsSuperAdmin,
    }