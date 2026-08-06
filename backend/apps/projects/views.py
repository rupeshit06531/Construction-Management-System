from rest_framework import generics

from apps.common.permissions import (
    IsManagerOrAbove,
    IsStaffUser,
    IsSuperAdmin,
)

from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.select_related("manager").all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsStaffUser]

        elif self.request.method == "POST":
            permission_classes = [IsManagerOrAbove]

        else:
            permission_classes = [IsManagerOrAbove]

        return [
            permission()
            for permission in permission_classes
        ]


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.select_related("manager").all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsStaffUser]

        elif self.request.method in ["PUT", "PATCH"]:
            permission_classes = [IsManagerOrAbove]

        elif self.request.method == "DELETE":
            permission_classes = [IsSuperAdmin]

        else:
            permission_classes = [IsStaffUser]

        return [
            permission()
            for permission in permission_classes
        ]