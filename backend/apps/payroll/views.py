from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Payroll
from .serializers import PayrollSerializer


@extend_schema(
    tags=["Payroll"],
    summary="Payroll management",
    description=(
        "Manage employee payroll records with search, filtering and ordering.\n"
        "Supports list, retrieve, create, update and delete operations."
    ),
)
class PayrollViewSet(
    RolePermissionMixin,
    ModelViewSet,
):

    queryset = Payroll.objects.select_related(
        "employee",
    ).all()

    serializer_class = PayrollSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "employee__email",
    ]

    filterset_fields = [
        "employee",
        "month",
        "status",
    ]

    ordering_fields = [
        "created_at",
        "month",
        "basic_salary",
        "bonus",
        "deduction",
        "net_salary",
    ]

    ordering = [
        "-month",
        "-created_at",
    ]

    role_permissions = {
        "list": IsAdminManagerEngineer,
        "retrieve": IsAdminManagerEngineer,
        "create": IsAdminOrManager,
        "update": IsAdminOrManager,
        "partial_update": IsAdminOrManager,
        "destroy": IsSuperAdmin,
    }