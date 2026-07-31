from django.db import models


class Employee(models.Model):

    class EmployeeType(models.TextChoices):
        ENGINEER = "ENGINEER", "Engineer"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        WORKER = "WORKER", "Worker"

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    employee_type = models.CharField(
        max_length=20,
        choices=EmployeeType.choices
    )

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )

    joining_date = models.DateField()

    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}"