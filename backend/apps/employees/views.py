from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Employee
from .serializers import EmployeeSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Employees"],
    summary="List and create employees",
    description=(
        "GET: Retrieve employees with search, filtering and ordering.\n"
        "POST: Create a new employee record."
    ),
)
class EmployeeListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):

    queryset = Employee.objects.all()

    serializer_class = EmployeeSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "employee_type",
    ]

    filterset_fields = [
        "employee_type",
    ]

    ordering_fields = [
        "created_at",
        "joining_date",
        "salary",
    ]

    ordering = [
        "-created_at",
    ]

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "POST": IsAdminOrManager,
    }


@extend_schema(
    tags=["Employees"],
    summary="Employee details",
    description=(
        "Retrieve, update or delete a single employee record."
    ),
)
class EmployeeDetailAPIView(
    RolePermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):

    queryset = Employee.objects.all()

    serializer_class = EmployeeSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }