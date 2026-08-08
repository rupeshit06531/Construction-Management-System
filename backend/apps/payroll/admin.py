from django.contrib import admin

from .models import Payroll


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "employee",
        "month",
        "basic_salary",
        "bonus",
        "deduction",
        "net_salary",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "month",
    ]

    search_fields = [
        "employee__first_name",
        "employee__last_name",
    ]