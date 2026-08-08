from decimal import Decimal

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.employees.models import Employee
from apps.expenses.models import Expense
from apps.inventory.models import Inventory
from apps.materials.models import Material
from apps.projects.models import Project
from apps.tasks.models import Task


User = get_user_model()


class DashboardAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="dashboard_user",
            email="dashboard@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "dashboard@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.project = Project.objects.create(
            name="Dashboard Project",
            code="DASH001",
            description="Dashboard test project",
            client="Dashboard Client",
            location="Ranchi",
            start_date="2026-08-01",
            end_date="2026-12-31",
            budget=Decimal("1000000.00"),
            status="ACTIVE",
            manager=self.user,
        )

    def test_dashboard_kpi(self):
        response = self.client.get(
            "/api/dashboard/kpi/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "total_projects",
            response.data,
        )

        self.assertIn(
            "total_employees",
            response.data,
        )

        self.assertIn(
            "total_tasks",
            response.data,
        )

        self.assertIn(
            "total_materials",
            response.data,
        )

        self.assertIn(
            "total_inventory_items",
            response.data,
        )

        self.assertIn(
            "total_expenses",
            response.data,
        )

        self.assertIn(
            "total_payroll",
            response.data,
        )

        self.assertEqual(
            response.data["total_projects"],
            1,
        )

        self.assertEqual(
            response.data["total_expenses"],
            "0.00",
        )

    def test_dashboard_kpi_expense_total(self):
        Expense.objects.create(
            project=self.project,
            title="Cement Purchase",
            category="MATERIAL",
            amount=Decimal("15000.00"),
            expense_date="2026-08-05",
        )

        Expense.objects.create(
            project=self.project,
            title="Transport Cost",
            category="TRANSPORT",
            amount=Decimal("5000.00"),
            expense_date="2026-08-06",
        )

        response = self.client.get(
            "/api/dashboard/kpi/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["total_expenses"],
            "20000.00",
        )

    def test_monthly_expenses(self):
        response = self.client.get(
            "/api/dashboard/monthly-expenses/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsInstance(
            response.data,
            list,
        )

        self.assertEqual(
            response.data,
            [],
        )

    def test_monthly_payroll(self):
        response = self.client.get(
            "/api/dashboard/monthly-payroll/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsInstance(
            response.data,
            list,
        )

    def test_monthly_payroll_aggregation(self):
        from decimal import Decimal

        from apps.employees.models import Employee
        from apps.payroll.models import Payroll

        employee = Employee.objects.create(
            first_name="Payroll",
            last_name="Dashboard Employee",
            employee_type="WORKER",
            phone="9876543210",
            email="payroll.dashboard@test.com",
            joining_date="2026-08-01",
            salary=Decimal("25000.00"),
        )

        Payroll.objects.create(
            employee=employee,
            month="2026-08-01",
            basic_salary=Decimal("25000.00"),
            bonus=Decimal("2000.00"),
            deduction=Decimal("1000.00"),
            net_salary=Decimal("26000.00"),
            status="PENDING",
        )

        Payroll.objects.create(
            employee=employee,
            month="2026-08-01",
            basic_salary=Decimal("30000.00"),
            bonus=Decimal("3000.00"),
            deduction=Decimal("1000.00"),
            net_salary=Decimal("32000.00"),
            status="PENDING",
        )

        response = self.client.get(
            "/api/dashboard/monthly-payroll/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["month"],
            "2026-08",
        )

        self.assertEqual(
            response.data[0]["total_payroll"],
            "58000.00",
        )


    def test_monthly_payroll(self):
        response = self.client.get(
            "/api/dashboard/monthly-payroll/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsInstance(
            response.data,
            list,
        )

    def test_monthly_payroll_aggregation(self):
        from decimal import Decimal

        from apps.employees.models import Employee
        from apps.payroll.models import Payroll

        employee = Employee.objects.create(
        first_name="Payroll",
        last_name="Dashboard Employee",
        employee_type="WORKER",
        phone="9876543210",
        email="payroll.dashboard@test.com",
        joining_date="2026-08-01",
        salary="25000.00",
    )

        Payroll.objects.create(
            employee=employee,
            month="2026-08-01",
            basic_salary=Decimal("25000.00"),
            bonus=Decimal("2000.00"),
            deduction=Decimal("1000.00"),
            net_salary=Decimal("26000.00"),
            status="PENDING",
        )

        Payroll.objects.create(
            employee=employee,
            month="2026-08-01",
            basic_salary=Decimal("30000.00"),
            bonus=Decimal("3000.00"),
            deduction=Decimal("1000.00"),
            net_salary=Decimal("32000.00"),
            status="PENDING",
        )

        response = self.client.get(
            "/api/dashboard/monthly-payroll/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["month"],
            "2026-08",
        )

        self.assertEqual(
            response.data[0]["total_payroll"],
            "58000.00",
        )

    def test_monthly_expenses_aggregation(self):
        Expense.objects.create(
            project=self.project,
            title="Cement Purchase",
            category="MATERIAL",
            amount=Decimal("10000.00"),
            expense_date="2026-08-05",
        )

        Expense.objects.create(
            project=self.project,
            title="Steel Purchase",
            category="MATERIAL",
            amount=Decimal("20000.00"),
            expense_date="2026-08-15",
        )

        Expense.objects.create(
            project=self.project,
            title="Transport Cost",
            category="TRANSPORT",
            amount=Decimal("5000.00"),
            expense_date="2026-09-05",
        )

        response = self.client.get(
            "/api/dashboard/monthly-expenses/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

        self.assertEqual(
            response.data[0]["month"],
            "2026-08",
        )

        self.assertEqual(
            response.data[0]["total_expense"],
            "30000.00",
        )

        self.assertEqual(
            response.data[1]["month"],
            "2026-09",
        )

        self.assertEqual(
            response.data[1]["total_expense"],
            "5000.00",
        )

    def test_dashboard_requires_authentication(self):
        self.client.credentials()

        response = self.client.get(
            "/api/dashboard/kpi/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_monthly_expenses_requires_authentication(self):
        self.client.credentials()

        response = self.client.get(
            "/api/dashboard/monthly-expenses/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_dashboard_customer_forbidden(self):
        customer = User.objects.create_user(
            username="dashboard_customer",
            email="customer_dashboard@test.com",
            password="password123",
            role="CUSTOMER",
        )

        self.client.force_authenticate(
            user=customer
        )

        response = self.client.get(
            "/api/dashboard/kpi/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_monthly_expenses_customer_forbidden(self):
        customer = User.objects.create_user(
            username="dashboard_customer_2",
            email="customer_dashboard_2@test.com",
            password="password123",
            role="CUSTOMER",
        )

        self.client.force_authenticate(
            user=customer
        )

        response = self.client.get(
            "/api/dashboard/monthly-expenses/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )