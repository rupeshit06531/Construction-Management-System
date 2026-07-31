from rest_framework import serializers

from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):

    material_name = serializers.CharField(
        source="material.name",
        read_only=True,
    )

    class Meta:
        model = Inventory

        fields = [
            "id",
            "material",
            "material_name",
            "transaction_type",
            "quantity",
            "remarks",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]