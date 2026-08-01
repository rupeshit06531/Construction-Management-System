from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import (
    IsAdminManagerEngineer,
    IsAdminOrManager,
    IsSuperAdmin,
)
from apps.common.mixins import RolePermissionMixin

from .models import Project
from .serializers import ProjectSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Projects"],
    summary="List and create projects",
    description=(
        "GET: Retrieve all projects with filtering, search and ordering.\n"
        "POST: Create a new construction project."
    ),
)
class ProjectListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):

    queryset = Project.objects.select_related(
        "manager"
    ).all()

    serializer_class = ProjectSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "name",
        "description",
        "status",
    ]

    filterset_fields = [
        "status",
        "manager",
    ]

    ordering_fields = [
        "created_at",
        "start_date",
        "end_date",
    ]

    ordering = [
        "-created_at",
    ]

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "POST": IsAdminOrManager,
    }


@extend_schema(
    tags=["Projects"],
    summary="Project details",
    description=(
        "Retrieve, update or delete a single project."
    ),
)
class ProjectDetailAPIView(
    RolePermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):

    queryset = Project.objects.select_related(
        "manager"
    ).all()

    serializer_class = ProjectSerializer

    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }