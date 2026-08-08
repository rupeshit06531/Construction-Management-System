from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


class IsProjectManagerOrAdmin(BasePermission):
    """
    Read access: Any authenticated user.
    Create/Update/Delete: SUPER_ADMIN, ADMIN, MANAGER.
    """

    allowed_roles = {
        "SUPER_ADMIN",
        "ADMIN",
        "MANAGER",
    }

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return request.user.role in self.allowed_roles


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.select_related("manager").all()
    serializer_class = ProjectSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectManagerOrAdmin,
    ]

    def perform_create(self, serializer):
        serializer.save()


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.select_related("manager").all()
    serializer_class = ProjectSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectManagerOrAdmin,
    ]