from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.select_related("manager").all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.select_related("manager").all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]