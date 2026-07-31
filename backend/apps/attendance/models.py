from django.db import models

from apps.employees.models import Employee


class Attendance(models.Model):

    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LEAVE = "LEAVE", "Leave"


    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
    )

    check_in = models.TimeField(
        blank=True,
        null=True,
    )

    check_out = models.TimeField(
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
        return f"{self.employee} - {self.date}"