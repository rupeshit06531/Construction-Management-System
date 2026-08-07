from django.db.models import Sum
from django.db.models.functions import TruncMonth

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from apps.accounts.permissions import IsAdminManagerEngineer
from apps.common.mixins import RolePermissionMixin
from apps.employees.models import Employee
from apps.expenses.models import Expense
from apps.inventory.models import Inventory
from apps.materials.models import Material
from apps.payroll.models import Payroll
from apps.projects.models import Project
from apps.tasks.models import Task

from .serializers import (
    DashboardKPISerializer,
    MonthlyExpenseSerializer,
    MonthlyPayrollSerializer,
)


@extend_schema(
    tags=["Dashboard"],
    summary="Dashboard KPI",
    description=(
        "Returns key performance indicators including "
        "projects, employees, tasks, materials, inventory, "
        "expenses and payroll."
    ),
    responses=DashboardKPISerializer,
)
class DashboardKPIAPIView(
    RolePermissionMixin,
    APIView,
):

    role_permissions = {
        "GET": IsAdminManagerEngineer,
    }

    def get(self, request):

        expense_total = (
            Expense.objects.aggregate(
                total=Sum("amount"),
            )["total"]
            or 0
        )

        payroll_total = (
            Payroll.objects.aggregate(
                total=Sum("net_salary"),
            )["total"]
            or 0
        )

        data = {
            "total_projects": Project.objects.count(),
            "total_employees": Employee.objects.count(),
            "total_tasks": Task.objects.count(),
            "total_materials": Material.objects.count(),
            "total_inventory_items": Inventory.objects.count(),
            "total_expenses": expense_total,
            "total_payroll": payroll_total,
        }

        serializer = DashboardKPISerializer(data)

        return Response(serializer.data)


@extend_schema(
    tags=["Dashboard"],
    summary="Monthly expense report",
    description=(
        "Returns monthly expense aggregation data."
    ),
    responses=MonthlyExpenseSerializer(many=True),
)
class MonthlyExpenseAPIView(
    RolePermissionMixin,
    APIView,
):

    role_permissions = {
        "GET": IsAdminManagerEngineer,
    }

    def get(self, request):

        queryset = (
            Expense.objects
            .annotate(
                month_key=TruncMonth("expense_date"),
            )
            .values("month_key")
            .annotate(
                total_expense=Sum("amount"),
            )
            .order_by("month_key")
        )

        data = [
            {
                "month": item["month_key"].strftime("%Y-%m"),
                "total_expense": item["total_expense"],
            }
            for item in queryset
        ]

        serializer = MonthlyExpenseSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)


@extend_schema(
    tags=["Dashboard"],
    summary="Monthly payroll report",
    description=(
        "Returns monthly payroll aggregation data."
    ),
    responses=MonthlyPayrollSerializer(many=True),
)
class MonthlyPayrollAPIView(
    RolePermissionMixin,
    APIView,
):

    role_permissions = {
        "GET": IsAdminManagerEngineer,
    }

    def get(self, request):

        queryset = (
            Payroll.objects
            .annotate(
                month_key=TruncMonth("month"),
            )
            .values("month_key")
            .annotate(
                total_payroll=Sum("net_salary"),
            )
            .order_by("month_key")
        )

        data = [
            {
                "month": item["month_key"].strftime("%Y-%m"),
                "total_payroll": item["total_payroll"],
            }
            for item in queryset
        ]

        serializer = MonthlyPayrollSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)