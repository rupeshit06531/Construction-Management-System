from django.conf import settings
from django.db import models


class Report(models.Model):

    class ReportType(models.TextChoices):
        PROJECT = "PROJECT", "Project Report"
        EMPLOYEE = "EMPLOYEE", "Employee Report"
        ATTENDANCE = "ATTENDANCE", "Attendance Report"
        PAYROLL = "PAYROLL", "Payroll Report"
        EXPENSE = "EXPENSE", "Expense Report"
        INVENTORY = "INVENTORY", "Inventory Report"
        MATERIAL = "MATERIAL", "Material Report"
        TASK = "TASK", "Task Report"
        DASHBOARD = "DASHBOARD", "Dashboard Report"

    title = models.CharField(
        max_length=255
    )

    report_type = models.CharField(
        max_length=20,
        choices=ReportType.choices
    )

    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_reports"
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    data = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title