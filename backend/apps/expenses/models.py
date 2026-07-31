from django.db import models

from apps.projects.models import Project


class Expense(models.Model):

    class ExpenseCategory(models.TextChoices):
        MATERIAL = "MATERIAL", "Material"
        LABOUR = "LABOUR", "Labour"
        EQUIPMENT = "EQUIPMENT", "Equipment"
        TRANSPORT = "TRANSPORT", "Transport"
        OTHER = "OTHER", "Other"


    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="expenses",
    )

    title = models.CharField(
        max_length=200,
    )

    category = models.CharField(
        max_length=20,
        choices=ExpenseCategory.choices,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    expense_date = models.DateField()

    description = models.TextField(
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
        return self.title