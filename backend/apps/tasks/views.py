from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.select_related(
        "project",
        "assigned_to",
    ).order_by("-created_at")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.select_related(
        "project",
        "assigned_to",
    ).all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]