from drf_spectacular.utils import extend_schema
from rest_framework import generics

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Attendance
from .serializers import AttendanceSerializer


@extend_schema(
    tags=["Attendance"],
    summary="List and create attendance records",
    description=(
        "GET: Retrieve attendance records.\n"
        "POST: Create a new attendance record."
    ),
)
class AttendanceListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):
    queryset = Attendance.objects.select_related(
        "employee",
    ).order_by("-date", "-created_at")

    serializer_class = AttendanceSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "POST": IsAdminOrManager,
    }


@extend_schema(
    tags=["Attendance"],
    summary="Attendance details",
    description=(
        "Retrieve, update or delete a single attendance record."
    ),
)
class AttendanceDetailAPIView(
    RolePermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = Attendance.objects.select_related(
        "employee",
    )

    serializer_class = AttendanceSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }