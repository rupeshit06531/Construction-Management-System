from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Payroll
from .serializers import PayrollSerializer
from drf_spectacular.utils import extend_schema


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

    queryset = Payroll.objects.all().order_by(
        "-created_at"
    )

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
    ]

    ordering_fields = [
        "created_at",
        "net_salary",
        "gross_salary",
    ]

    ordering = [
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