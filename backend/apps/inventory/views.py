from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Inventory
from .serializers import InventorySerializer


class InventoryListCreateAPIView(generics.ListCreateAPIView):

    queryset = Inventory.objects.select_related(
        "material"
    ).all()

    serializer_class = InventorySerializer

    permission_classes = [
        IsAuthenticated
    ]


class InventoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Inventory.objects.select_related(
        "material"
    ).all()

    serializer_class = InventorySerializer

    permission_classes = [
        IsAuthenticated
    ]