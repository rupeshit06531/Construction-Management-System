from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Material
from .serializers import MaterialSerializer


class MaterialListCreateAPIView(generics.ListCreateAPIView):
    queryset = Material.objects.select_related(
        "project",
    ).order_by("-created_at")
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]


class MaterialDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.select_related(
        "project",
    ).all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]