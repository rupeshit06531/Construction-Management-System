from django.db import models

from apps.materials.models import Material


class Inventory(models.Model):

    class TransactionType(models.TextChoices):
        IN = "IN", "Stock In"
        OUT = "OUT", "Stock Out"


    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="inventory_transactions",
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    def __str__(self):
        return f"{self.material.name} - {self.transaction_type}"