from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Expense
from .serializers import ExpenseSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Expenses"],
    summary="Expense management",
    description=(
        "Manage project expenses with search, filtering and ordering.\n"
        "Supports list, retrieve, create, update and delete operations."
    ),
)
class ExpenseViewSet(
    RolePermissionMixin,
    ModelViewSet,
):

    queryset = Expense.objects.all().order_by(
        "-created_at"
    )

    serializer_class = ExpenseSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "description",
        "category",
    ]

    filterset_fields = [
        "category",
        "project",
        "created_at",
    ]

    ordering_fields = [
        "created_at",
        "amount",
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