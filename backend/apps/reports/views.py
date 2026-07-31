from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.projects.models import Project
from apps.employees.models import Employee
from apps.expenses.models import Expense
from apps.payroll.models import Payroll

from .serializers import ReportSerializer


class DashboardReportAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

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

        return Response(
            serializer.data
        )