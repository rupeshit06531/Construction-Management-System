from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Attendance
from .serializers import AttendanceSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Attendance"],
    summary="List and create attendance records",
    description=(
        "GET: Retrieve attendance records with search, filtering and ordering.\n"
        "POST: Create a new attendance record."
    ),
)
class AttendanceListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):

    queryset = Attendance.objects.select_related(
        "employee"
    ).all()

    serializer_class = AttendanceSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "status",
    ]

    filterset_fields = [
        "employee",
        "status",
        "date",
    ]

    ordering_fields = [
        "date",
        "created_at",
    ]

    ordering = [
        "-date",
    ]

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
        "employee"
    ).all()

    serializer_class = AttendanceSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }