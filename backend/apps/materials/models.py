from django.db import models

from apps.projects.models import Project


class Material(models.Model):

    class Category(models.TextChoices):
        CEMENT = "CEMENT", "Cement"
        STEEL = "STEEL", "Steel"
        BRICKS = "BRICKS", "Bricks"
        SAND = "SAND", "Sand"
        OTHER = "OTHER", "Other"


    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="materials",
    )

    name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )

    unit = models.CharField(
        max_length=50
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    supplier = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.name