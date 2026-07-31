from django.db import models

from apps.employees.models import Employee


class Payroll(models.Model):

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"


    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payrolls",
    )

    month = models.DateField()

    basic_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    bonus = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    deduction = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    net_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    payment_date = models.DateField(
        blank=True,
        null=True,
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
        return f"{self.employee} - {self.month}"