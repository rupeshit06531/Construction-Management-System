from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminManagerEngineer
from apps.common.mixins import RolePermissionMixin
from apps.employees.models import Employee
from apps.expenses.models import Expense
from apps.payroll.models import Payroll
from apps.projects.models import Project

from .serializers import ReportSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Reports"],
    summary="Dashboard report",
    description=(
        "Returns summary report data including projects, "
        "employees, expenses and payroll statistics."
    ),
    responses=ReportSerializer(many=True),
)
class DashboardReportAPIView(
    RolePermissionMixin,
    APIView,
):

    role_permissions = {
        "GET": IsAdminManagerEngineer,
    }

    def get(self, request):

        data = [
            {
                "title": "Total Projects",
                "total": Project.objects.count(),
            },
            {
                "title": "Total Employees",
                "total": Employee.objects.count(),
            },
            {
                "title": "Total Expenses",
                "amount": sum(
                    Expense.objects.values_list(
                        "amount",
                        flat=True,
                    )
                ),
            },
            {
                "title": "Total Payroll Records",
                "total": Payroll.objects.count(),
            },
        ]

        serializer = ReportSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)