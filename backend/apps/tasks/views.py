from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Task
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Tasks"],
    summary="List and create tasks",
    description=(
        "GET: Retrieve tasks with search, filtering and ordering.\n"
        "POST: Create a new project task."
    ),
)
class TaskListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):

    queryset = Task.objects.select_related(
        "project",
        "assigned_to",
    ).all()

    serializer_class = TaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "description",
        "status",
    ]

    filterset_fields = [
        "status",
        "priority",
        "project",
        "assigned_to",
    ]

    ordering_fields = [
        "created_at",
        "due_date",
    ]

    ordering = [
        "-created_at",
    ]

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "POST": IsAdminOrManager,
    }


@extend_schema(
    tags=["Tasks"],
    summary="Task details",
    description=(
        "Retrieve, update or delete a single task."
    ),
)
class TaskDetailAPIView(
    RolePermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):

    queryset = Task.objects.select_related(
        "project",
        "assigned_to",
    ).all()

    serializer_class = TaskSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }