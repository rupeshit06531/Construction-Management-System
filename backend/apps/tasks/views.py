from rest_framework import generics

from apps.common.mixins import RolePermissionMixin
from apps.common.permissions import (
    IsManagerOrAbove,
    IsStaffUser,
    IsSuperAdmin,
)

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateAPIView(
    RolePermissionMixin,
    generics.ListCreateAPIView,
):
    queryset = Task.objects.select_related(
        "project",
        "assigned_to",
    ).order_by("-created_at")

    serializer_class = TaskSerializer

    role_permissions = {
        "GET": IsStaffUser,
        "POST": IsManagerOrAbove,
    }


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
        "GET": IsStaffUser,
        "PUT": IsManagerOrAbove,
        "PATCH": IsManagerOrAbove,
        "DELETE": IsSuperAdmin,
    }